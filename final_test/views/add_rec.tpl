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
<br>
<br>

<form action="/add_rec" method="post">
<div class="row">
  <div class="column">
  <label for="rname">Recipe Name (Max 900 Characters):</label><br>
  <input type="text" id="rname" name="rname"><br><br>

  <label for="author">Author (Max 100 Charcters):</label><br>
  <input type="text" id="author" name="author"><br><br>

  <label for="source">Source (Max 100 Characters - Must Include):</label><br>
  <input type="text" id="source" name="source"><br><br>

  <label for="url"> URL (.com Only):</label><br>
  <input type="text" id="url" name="url"><br><br>

  <label for="cuisine"> Cuisine (Max 150 Characters):</label><br>
  <input type="text" id="cuisine" name="cuisine"><br><br>

  <label for="time">Cook Time (Integer in Minutes):</label><br>
  <input type="text" id="time" name="time"><br><br>
</div>

  <div class="column">
  <label for="cals">Calories (Integer):</label><br>
  <input type="text" id="cals" name="cals" ><br><br>

  <label for="comp">Complexity (High, Medium, or Low):</label><br>
    <input type="text" id="comp" name="comp">
<br><br>
  <label for="type">Type of Dish (Max 15 Characters):</label><br>
  <input type="text" id="type" name="type" ><br><br>

  <label for="veg">Veg Status (Vegan, Vegetarian, or Neither):</label><br>
<input type="text" id="veg" name="veg" >
<br><br>
  <label for="spicy">Spiciness (High, Medium, or Low):</label><br>
<input type="text" id="spicy" name="spicy" ><br><br>
<input type="submit" value="Submit">
</div>
<br><br><br><br>

</form>

% include('footer.tpl')