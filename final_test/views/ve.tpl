% include('header.tpl')
<!-- Main content should go here-->
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

<form action="/update" method="post">

<input type="hidden" id = "id" name = "id" value = {{ recipe[0] }}>
<div class="row">
  <div class="column">
  <label for="rname">Recipe Name (Max 900 Characters):</label><br>
  <input type="text" id="rname" name="rname" value = "{{ recipe[1] }}"><br><br>

  <label for="author">Author (Max 100 Charcters):</label><br>
  <input type="text" id="author" name="author" value = "{{ recipe[2] }}"><br><br>

  <label for="source">Source (Max 100 Characters - Must Include):</label><br>
  <input type="text" id="source" name="source" value = "{{ recipe[3] }}"><br><br>

  <label for="url"> URL (.com Only):</label><br>
  <input type="text" id="url" name="url" value = "{{ recipe[4] }}"><br><br>

  <label for="cuisine"> Cuisine (Max 150 Characters):</label><br>
  <input type="text" id="cuisine" name="cuisine" value = "{{ recipe[5] }}"><br><br>

  <label for="time">Cook Time (Integer in Minutes):</label><br>
  <input type="text" id="time" name="time" value = "{{ recipe[6] }}"><br><br>
</div>

  <div class="column">
  <label for="cals">Calories (Integer):</label><br>
  <input type="text" id="cals" name="cals" value = "{{ recipe[7] }}"><br><br>

  <label for="comp">Complexity (High, Medium, or Low):</label><br>
    <input type="text" id="comp" name="comp" value = "{{ recipe[8] }}">
<br><br>
  <label for="type">Type of Dish (Max 15 Characters):</label><br>
  <input type="text" id="type" name="type" value = "{{ recipe[9] }}"><br><br>

  <label for="veg">Veg Status (Vegan, Vegetarian, or Neither):</label><br>
<input type="text" id="veg" name="veg" value = "{{ recipe[10] }}">
<br><br>
  <label for="spicy">Spiciness (High, Medium, or Low):</label><br>
<input type="text" id="spicy" name="spicy" value = "{{ recipe[11] }}">
<br><br><br>
  <input type="submit" value="Submit">
  </div>
</form>

% include('footer.tpl')