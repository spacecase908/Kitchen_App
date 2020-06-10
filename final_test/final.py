from bottle import Bottle, post, get, HTTPResponse, request, response, template
import bottle
import os
import sys
import psycopg2 as pg
import logging
import argparse
import random


#The logging level to control what messages are shown (skipping debug)
logging.basicConfig(level=logging.INFO)

#Our bottle app, using the default. We can store variables in app
app = bottle.default_app()

@get("/")
def home():
    # home page!
    # Display search boxes for the user to select what recipe they would like to see
    # User can also add recipe via the header

    return template('home',
                    page_name='Recipe Database Home Page',
                    body='Bon Apetit!')

@post("/results")
def results():
    # get the search terms from the form
    recipe_name = request.forms.get('rname')
    rec_id = request.forms.get('rid')
    rec_veg = request.forms.get('veg')
    cuisine = request.forms.get('cuisine')
    id = request.forms.get('id')
    if id:
        try:
            cur = app.db_connection.cursor()
            SQL = "SELECT count(rec_id) from recipe;"
            cur.execute(SQL)
            cnt = cur.fetchone()[0]
            rec_id = random.randint(1,cnt)
            app.db_connection.commit()
            cur.close()
        except Exception as e:
            app.db_connection.rollback()
            errors = [str(e)]
            cur.close()
            return template('error',
                            page_name='Search Error',
                            body='Your search could not be completed.',
                            instructions='See the error messages below and try again!',
                            errors=errors)


    # both recipe name and cuisine will be wildcard variables. In order to do the like search, I am reformatting the
    # search term here to include the % sign. This simplifies things when building the prepared statements. I got the idea
    # from here: https://stackoverflow.com/questions/37273237/how-to-use-like-pattern-matching-with-postgresql-and-python-with-multiple-percen

    if recipe_name:
        recipe_name = '%{}%'.format(recipe_name)
    if cuisine:
        cuisine = '%{}%'.format(cuisine)

    # if no forms are submitted, return an error to the user
    if not recipe_name and not rec_id and not cuisine:
        return template('error',
                        page_name='ERROR',
                        body='No search terms!',
                        instructions='Return to the home page and perform another search',
                        errors='')

    # set up cursor
    cur = app.db_connection.cursor()
    # since rec ID is the primary key, if a user searches on that other keys are either unessesary or will potentially produce errors
    # I've informed the user on the front page that if the primary key is searched on, other keys will be ignored to avoid conflicts
    if rec_id:
        SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE rec_id = %s order by rec_id desc;"
        data = (rec_id,)
    elif rec_veg != 'Any':
        if cuisine and recipe_name:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(rec_name) like %s and lower(cuisine) like %s and vegetarian_status =%s order by rec_id desc;"
            data = (recipe_name, cuisine, rec_veg)
        elif cuisine:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(cuisine) like %s and vegetarian_status =%s order by rec_id desc;"
            data = (cuisine, rec_veg)
        elif recipe_name:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(rec_name) like %s and vegetarian_status =%s order by rec_id desc;"
            data = (recipe_name, rec_veg)
    else:
        if cuisine and recipe_name:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(rec_name) like %s and lower(cuisine) like %s order by rec_id desc;"
            data = (recipe_name, cuisine)
        elif cuisine:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(cuisine) like %s order by rec_id desc;"
            data = (cuisine, )
        elif recipe_name:
            SQL = "SELECT rec_id, rec_name, author, cuisine,vegetarian_status FROM recipe WHERE lower(rec_name) like %s order by rec_id desc;"
            data = (recipe_name, )
    try:
        cur.execute(SQL,data)
        response = cur.fetchmany(20)
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Search Error',
                        body='Your search could not be completed.',
                        instructions='See the error messages below.',
                        errors=errors)

    cur.close()
    if len(response) == 0:
        return template('error',
                        page_name='No Results',
                        body='The search terms you entered yielded no results',
                        instructions='Return to the home page and try again!',
                        errors='')
    return template('results',
                    page_name='Recipe Results',
                    body='These recipes meet your search criteria',
                    recipes=response)


@get("/ve/<id:int>")
def ve(id):
    rec_id = str(id)
    cur = app.db_connection.cursor()

    SQL = "SELECT * FROM recipe WHERE rec_id = %s;"
    data = (rec_id,)
    try:
        cur.execute(SQL,data)
        response = cur.fetchmany(20)
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Error',
                        body='Your search could not be completed due to an error. Please see errors below',
                        errors=errors,
                        instructions='')

    if len(response) == 0:
        return template('error',
                        page_name = 'No Results',
                        body="Unfortunately the recipe you selected does not appear to exist.",
                        instructions='Please try again or select another recipe.',
                        errors='')

    return template('ve',
                    page_name=f"View/Edit {response[0][1]}",
                    recipe = response[0])

@post("/update")
def ve():
    valid = ['High', "Low", "Medium"]
    validv = ['Vegan', 'Vegetarian', 'Neither']
    rec_name = request.forms.get('rname')
    author = request.forms.get('author')
    source = request.forms.get('source')
    url = request.forms.get('url')
    cuisine = request.forms.get('cuisine')
    cook_time = request.forms.get('time')
    cals = request.forms.get('cals')
    comp = request.forms.get('comp').capitalize()
    type = request.forms.get('type')
    veg = request.forms.get('veg').capitalize()
    spicy = request.forms.get('spicy').capitalize()
    curr_id = request.forms.get('id')
    errors = []

    # error handling:
        # first, if the ID has been changed, confirm no other relation has that ID
        # as the ID is the primary key and must be unique
        # if so, do not process this update and show user to an error page

    # next, confirm cook time is a number and integer
    if not cook_time.isdigit():
        errors.append("The cook time must be an integer.")
    # next, confirm calories is a number and integer
    if not cals.isdigit():
        errors.append("The calorie value must be an integer.")

    # Check to make sure data constraints are met
    if not rec_name or len(rec_name) > 900:
        errors.append("The recipe must have a name and it must be less than 900 characters.")
    if len(author) > 100:
        errors.append("The author's name must have less than 100 characters.")
    if len(cuisine) > 150:
        errors.append("The cuisine name must have less than 150 characters.")
    if not source or len(source) > 100:
        errors.append("The recipe must have a source, and source must have less than 100 charactes")
    if len(type) > 15:
        errors.append("The recipe type must have less than 15 characters")
    # Maintain common formatting for comp, spicy, and vegan
    if veg not in validv:
        errors.append("The recipe should be either Vegan, Vegetarian, or Neither.")
    if comp not in valid:
        errors.append("The complexity should be either High, Medium, or Low.")
    if ".com" not in url:
        errors.append('The domain for the url must be a .com')
    if spicy not in valid:
        errors.append("The spiciness should be either High, Medium, or Low.")

    if len(errors) > 0:
        return template('error',
                        page_name="View/Edit Error",
                        body= 'We had some issues with your submission.',
                        instructions= 'Please see the errors below',
                        errors=errors)
    else:
        SQL = "UPDATE recipe SET rec_name=%s, author=%s, source=%s, url=%s, cuisine=%s, time_to_cook=%s, calories=%s,complexity=%s,type=%s,vegetarian_status=%s,spiciness=%s where rec_id=%s"
        data = (rec_name,author,source,url,cuisine,cook_time,cals,comp,type,veg,spicy,curr_id)
        try:
            cur = app.db_connection.cursor()
            cur.execute(SQL, data)
            app.db_connection.commit()
        except Exception as e:
            app.db_connection.rollback()
            errors = [str(e)]
            cur.close()
            return template('error',
                            page_name='Search Error',
                            body='Your seach could not be completed.',
                            instructions='See the error messages below.',
                            errors=errors)
        return template('home',
                        page_name='Recipe Database Home Page',
                        body=f"Your update to {rec_name} has been completed!")


@get("/ings/<id>")
def ings(id):
    # view edit
    # Show a table of all ingredients in the relation with name, quantity have, quantity required? Maybe color, type
    #search text
    rec_id = str(id)
    SQL = "SELECT i.ing_id, i.ing_name, i.type, i.color, i.quantity, i.expiration_date, ir.qty, r.rec_name FROM ingredient i INNER JOIN ing_required ir on i.ing_id = ir.ing_id INNER JOIN recipe r on r.rec_id = ir.rec_id WHERE r.rec_id =%s order by i.ing_id desc;"
    data = (rec_id,)
    try:
        cur = app.db_connection.cursor()
        cur.execute(SQL,data)
        response = cur.fetchmany(20)
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Search Error',
                        body='Your search could not be completed.',
                        instructions='See the error messages below.',
                        errors=errors)

    if len(response) == 0:
        return template('error',
                        page_name='No Ingredients',
                        body='This recipe currently has no ingredients.',
                        instructions='Return to the previous page and select "Add new ingredient" to help complete the recipe!',
                        errors='')
    return template('ing_results',
                    page_name=f"ingredients for {response[0][7]}",
                    ingredients=response)

@get("/add_ing/<id>")
def add(id):
    rec_id = id
    SQL = "SELECT distinct i.ing_name, i.ing_id FROM ingredient i INNER JOIN ing_required ir on i.ing_id = ir.ing_id INNER JOIN recipe r on r.rec_id = ir.rec_id WHERE r.rec_id !=%s order by i.ing_id desc;"
    data = (rec_id,)
    cur = app.db_connection.cursor()
    try:
        cur.execute(SQL,data)
        response = cur.fetchmany(20)
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Search Error',
                        body='Your search could not be completed.',
                        instructions='See the error messages below.',
                        errors=errors)

    return template('add_ing',
                    page_name='Add Ingredients',
                    body='Select an ingredient to add to this recipe',
                    ings = response,
                    rec_id = rec_id)

@post("/add_ing")
def add():
    ing_id = request.forms.get('ing_id')
    rec_id = request.forms.get('id')
    qty = request.forms.get('qty')

    errors = []
    # So at this point, in theory unless someone is sending fake post requests, we should be sure of a few things:
    # the ingredient is not already in the recipe, as those were filtered out and not given as options
    # also, the ingredient ID and recipe ID are both real and in the correct format,
    # as I am passing those myself and they are not entered by the user
    # In theory, the only one that is suspect is the quantity.
    # Nevertheless, I will run error checking to make sure they are in the right format
    # I am for now assuming that multiple users won't be using the app simulatneoulsy and changing things while someone
    # is trying to edit this ingredient
    if not ing_id.isdigit():
        errors.append('The ingredient you have selected is not valid')
    if not qty:
        errors.append('No quantity has been provided')
    if not qty.isnumeric():
        errors.append('The quanity you entered is not valid')
    #error handling for names, id's, and rec ID
    if len(errors) > 0:
        return template('errors',
                        page_name='Ingredient Add Failed',
                        body='Unfortunately we were not able to add this ingredient to the database.',
                        instructions='Please try again for a different ingredient, after correcting the errors below.',
                        errors=errors)


    SQL = "INSERT INTO ing_required(rec_id,ing_id,qty) VALUES (%s,%s,%s)"
    data = (rec_id,ing_id,qty)
    cur = app.db_connection.cursor()
    try:
        cur.execute(SQL,data)
        app.db_connection.commit()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Error',
                        body='Your ingredient could not be added.',
                        instructions='See the error messages below.',
                        errors=errors)

    return template('home',
                    page_name='Recipe Database Home Page',
                    body="Your ingredient has been successfully added.")

@post("/new_ing")
def new_ing():
    ing_name = request.forms.get('iname')
    quantity = request.forms.get('qty')
    family = request.forms.get('family')
    color = request.forms.get('color')
    organic = request.forms.get('org')
    loc = request.forms.get('loc')
    sea = request.forms.get('sea')
    qual = request.forms.get('quality')
    sto = request.forms.get('sto')
    exp = request.forms.get('exp')
    qty = request.forms.get('quantity')
    rec_id = request.forms.get('id')
    typ = request.forms.get('type')
    errors = []

    if not ing_name or len(ing_name) > 100:
        errors.append("The ingredient needs a name that is less than 100 characters")
    if not quantity.isnumeric():
        errors.append('You must include a numeric quantity of the ingredient')
    if len(family) > 25:
        errors.append('The family name must be less than 25 characters')
    if len(color) > 25:
        errors.append('The color must be less than 25 characters')
    if len(loc)> 25:
        errors.append('The location must be less than 25 characters')
    if not qty.isnumeric():
        errors.append('You must include a numeric quantity of the ingredient')
    if len(sea)>25:
        errors.append('The season must be less than 25 characters')
    if len(typ) > 25:
        errors.append('The ingredient type must be less than 25 characters')
    if len(errors) > 0:
        return template('error',
                        page_name='Error',
                        body='Your ingredient could not be added.',
                        instructions='See the error messages below.',
                        errors=errors)

    SQL1 = "INSERT INTO ingredient(ing_name,quantity,family,color,organic,Expiration_date,Location_purchased,Season,quality,Storage_id,type) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING ing_id;"
    data1 = (ing_name,quantity,family,color,organic,exp,loc,sea,qual,sto,typ)
    SQL2 = "INSERT INTO ing_required (rec_id,ing_id,qty) VALUES (%s,%s,%s);"

    try:
        cur = app.db_connection.cursor()
        cur.execute(SQL1, data1)
        ing_id = cur.fetchone()[0]
        data2 = (rec_id,ing_id,qty)
        cur.execute(SQL2,data2)
        app.db_connection.commit()
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Error',
                        body='Your ingredient could not be added.',
                        instructions='See the error messages below.',
                        errors=errors)

    return template('home',
                    page_name='Recipe Database Home Page',
                    body="You're ingredient has been successfully added.")







@get("/add_rec")
def add():
    return template('add_rec',
                    page_name='New Recipe!',
                    body='Fill out the forms below!')

@post("/add_rec")
def add():
    valid = ['High', "Low", "Medium"]
    validv = ['Vegan', 'Vegetarian', 'Neither']
    rec_name = request.forms.get('rname')
    author = request.forms.get('author')
    source = request.forms.get('source')
    url = request.forms.get('url')
    cuisine = request.forms.get('cuisine')
    cook_time = request.forms.get('time')
    cals = request.forms.get('cals')
    comp = request.forms.get('comp').capitalize()
    type = request.forms.get('type')
    veg = request.forms.get('veg').capitalize()
    spicy = request.forms.get('spicy').capitalize()

    errors = []


    # error handling:
    # first, if the ID has been changed, confirm no other relation has that ID
    # as the ID is the primary key and must be unique
    # if so, do not process this update and show user to an error page


    # next, confirm cook time is a number and integer
    if not cook_time.isdigit():
        errors.append("The cook time must be an integer.")
    # next, confirm calories is a number and integer
    if not cals.isdigit():
        errors.append("The calorie value must be an integer.")

    if not rec_name or len(rec_name) > 900:
        errors.append("The recipe must have a name and it must be less than 900 characters.")
    if len(author) > 100:
        errors.append("The author's name must have less than 100 characters.")
    if len(cuisine) > 150:
        errors.append("The cuisine name must have less than 150 characters.")
    if not source or len(source) > 100:
        errors.append("The recipe must have a source, and source must hace less than 100 charactes")
    if len(type) > 15:
        errors.append("The recipe type must have less than 15 characters")
    if veg not in validv:
        errors.append("The recipe should be either Vegan, Vegetarian, or Neither.")
    if comp not in valid:
        errors.append("The complexity should be either High, Medium, or Low.")
    if spicy not in valid:
        errors.append("The spiciness should be either High, Medium, or Low.")
    if len(errors) > 0:
        return template('errors',
                        page_name="View/Edit Error",
                        body='We had some issues with your submission.',
                        instructions='Please see the errors below and try again',
                        error=errors)
    else:
        SQL = "INSERT INTO recipe(rec_name,Author,Source,url,cuisine,time_to_cook,calories,complexity,type,vegetarian_status,spiciness) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data = (rec_name,author,source,url,cuisine,cook_time,cals,comp,type,veg,spicy)
        cur = app.db_connection.cursor()
        try:
            cur.execute(SQL, data)
            app.db_connection.commit()
        except Exception as e:
            app.db_connection.rollback()
            errors = [str(e)]
            cur.close()
            return template('error',
                            page_name='Search Error',
                            body='Your request could not be completed.',
                            instructions='See the error messages below.',
                            errors=errors)

    return template('home',
                    page_name='Recipe Database Home Page',
                    body=f"{rec_name} has been successfully added.")

@get("/delete/<id>")
def delete(id):
    rec_id = id
    cur = app.db_connection.cursor()
    SQL = "DELETE FROM recipe WHERE rec_id = %s"
    data = (rec_id,)
    try:
        cur.execute(SQL, data)
        app.db_connection.commit()
        cur.close()
    except Exception as e:
        app.db_connection.rollback()
        errors = [str(e)]
        cur.close()
        return template('error',
                        page_name='Search Error',
                        body='Your seach could not be completed.',
                        instructions='See the error messages below.',
                        errors=errors)
    return template('delete',
                    page_name='Recipe Deleted!',
                    body=f'Recipe ID {rec_id} has been deleted from the database.')


#The main function to start the server
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c","--config",
        help="The path to the .conf configuration file.",
        default="server.conf"
    )
    parser.add_argument(
        "--host",
        help="Server hostname (default localhost)",
        default="localhost"
    )
    parser.add_argument(
        "-p","--port",
        help="Server port (default 53001)",
        default=53001,
        type=int
    )
    parser.add_argument(
        "--nodb",
        help="Disable DB connection on startup",
        action="store_true"
    )

    #Get the arguments
    args = parser.parse_args()
    if not os.path.isfile(args.config):
        logging.error("The file \"{}\" does not exist!".format(args.config))
        sys.exit(1)

    app.config.load_config(args.config)

    # Below is how to connect to a database. We put a connection in the default bottle application, app
    if not args.nodb:
        try:
            app.db_connection = pg.connect(
                dbname = app.config['db.dbname'],
                user = app.config['db.user'],
                password = app.config.get('db.password'),
                host = app.config['db.host'],
                port = app.config['db.port']
            )
        except KeyError as e:
            logging.error("Is your configuration file ({})".format(args.config) +
                        " missing options?")
            raise

    try:
        logging.info("Starting Bottle Web Server")
        app.run(host=args.host, port=args.port, debug=True)
        app.db_connection.rollback()
        app.db_connection.close()
    finally:
        #Ensure that the connection opened is closed
        if not args.nodb:
            app.db_connection.close()
