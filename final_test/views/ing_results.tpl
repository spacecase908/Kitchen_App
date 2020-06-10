% include('header.tpl')
<!-- Main content should go here-->

<h1>{{ page_name }}</h1>
<br>

    <div class="row">
      <div class="col-md-12">
        <% if ingredients: %>
          <table class="table">
            <th class="col-md-2 text-left">Ingredient Name</th>
            <th class="col-md-1 text-left">Type</th>
            <th class="col-md-1 text-left">Color</th>
            <th class="col-md-1 text-left">Required</th>
            <th class="col-md-1 text-left">In Stock</th>
            <th class="col-md-1 text-left">Expiration Date</th>
            <% for ing in ingredients: %>
              <tr>
                <td class="col-md-1 text-left">
                  {{ ing[1] }}
                </td>
                <td class="col-md-1 text-left">
                    {{ ing[2] }} </td>
                <td class="col-md-1 text-left">
                    {{ ing[3] }}</td>
                <td class="col-md-1 text-left">
                    {{ ing[6] }}</td>
                <td class="col-md-1 text-left">
                    {{ ing[4] }}</td>
                <td class="col-md-1 text-left">
                    {{ ing[5] }}</td>

              </tr>
              % end
          </table>
      </div>
    </div>
    % include('footer.tpl')