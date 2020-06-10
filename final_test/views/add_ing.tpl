% include('header.tpl')
<!-- Main content should go here-->
<!-- from w3c website: https://www.w3schools.com/howto/howto_css_two_columns.asp-->
<style>
* {
  box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
  float: left;
  width: 50%;
  padding: 10px;
  height: 300px; /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>
<h1>{{ page_name }}</h1>

<h3>You may add an existing ingredient to the recipe, or create a new one.</h3>
<br><br>
<h4>Add Existing Ingredient:</h4>
<form action="/add_ing" method="post">
<input type="hidden" id = "id" name = "id" value = {{ rec_id }}>
<label for="ing_id">Ingredients:</label>
    <select id="ing_id" name="ing_id">
    <% for ing in ings: %>
    <option value={{ ing[1] }}>{{ ing[0] }}</option>
    % end
    </select>
<label for="qty">Quantity Required:</label>
  <input type="text" id="qty" name="qty"><br><br>
  <input type="submit" value="Submit">
</form>


<br><br>
<h4>Create a new Ingredient:</h4><br>

<form action="/new_ing" method="post">
<input type="hidden" id = "id" name = "id" value = {{ rec_id }}>

<div class="row">
  <div class="column">

<label for="iname">Ingredient Name (Max 100 Characters):</label><br>
<input type="text" id="iname" name="iname">  <br><br>

<label for="qty">Quantity in Stock (Number - Must Include):</label><br>
<input type="text" id="qty" name="qty"><br><br>

   <label for="quantity">Quantity Required (Number - Must Include):</label><br>
  <input type="text" id="quantity" name="quantity"><br><br>

  <label for="type">Type (Max 25 Characters):</label><br>
  <input type="text" id="type" name="type"><br><br>

  <label for="family">Family (Max 25 Characters):</label><br>
  <input type="text" id="family" name="family""><br><br>

  <label for="color">Color (Max 25 Characters):</label><br>
  <input type="text" id="color" name="color"><br><br>
  </div>

  <div class="column">

    <label for="org">Organic (True or False):</label><br>
    <select id="org" name="org">
    <option value="True">True</option>
    <option value="False">Vegan</option>
    </select><br><br>

  <label for="loc">Location Purchased (Max 25 Characters):</label><br>
  <input type="text" id="loc" name="loc""><br><br>

  <label for="sea">Season (Max 25 Characters):</label><br>
  <input type="text" id="sea" name="sea"><br><br>

  <label for="quality">Quality (Max 25 Characters):</label><br>
    <input type="text" id="quality" name="quality"><br><br>

   <label for="sto">Storage Location:</label><br>
    <select id="sto" name="sto">
    <option value="17">Pantry</option>
    <option value="1">Refrigerator</option>
    <option value="6">Deep Freezer</option>
    </select><br><br>

       <label for="exp">Expiration:</label><br>
    <select id="exp" name="exp">
    <option value="6/13/2020">1 Week</option>
    <option value="6/20/2020">2 Weeks</option>
    <option value="7/6/2020">1 Month</option>
    <option value="6/6/2021">1 Year</option>
    </select>
<br><br>

</div>
</div>



<br><br><br><br><br><br><br><br>
<input type="submit" value="Submit">
</form>

% include('footer.tpl')