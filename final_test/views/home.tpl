% include('header.tpl')
<!-- Main content should go here-->

<h1>{{ page_name}}</h1>
<h2>{{ body }}<h2>
<br>
<h3>If you are feeling adventurous, pick a random recipe!
 <br><br>
  <form action="/results" method="post">
 <label for="rid">Random Recipe:</label>
<input type="hidden" id = "id" name = "id" value = 'random'>
  <input type="submit" value="Get Lucky!">
  </form><br>
  If you know what you are looking for, try searching below! <br><br>
 <form action="/results" method="post">
  <label for="rname">*Recipe Name*:</label><br>
  <input type="text" id="rname" name="rname"><br><br>
  <label for="rname">*Cuisine*:</label><br>
  <input type="text" id="cuisine" name="cuisine"><br><br>
   <label for="veg">Veg Status:</label><br>
    <select id="veg" name="veg">
    <option value="Any">Any</option>
    <option value="Vegan">Vegan</option>
    <option value="Vegetarian">Vegetarian</option>
    <option value="Neither">Neither</option>
    </select>
  <br><br><br>
  <input type="submit" value="Submit">
</form>

% include('footer.tpl')
