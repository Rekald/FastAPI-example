function del_row(row_id){
    let xhr = get_json_ajax("DELETE", '/inventory/row?row_id=' + row_id);

    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#inventory_table').DataTable().ajax.reload();
        }
    }

    xhr.send(JSON.stringify({}));
}

function update_row(){
    let id = document.getElementById("id_edit").value;
    let part_code = document.getElementById("part_code_edit").value;
    let description = document.getElementById("description_edit").value;
    let producer = document.getElementById("producer_edit").value;
    let quantity_str = document.getElementById("quantity_edit").value;
    let catalog_price_str = document.getElementById("catalog_price").value;
    let discount_str = document.getElementById("discount_edit").value;

    let quantity = parseInt(quantity_str);
    let catalog_price = parseFloat(catalog_price_str);
    let discount = parseFloat(discount_str);

    let buy_price = catalog_price * (1 - discount/100);
    let total_value = buy_price * quantity;

    let data = {
        id: id,
        part_code : part_code,
        description : description,
        producer : producer,
        quantity : quantity,
        catalog_price : catalog_price,
        discount : discount,
        buy_price: buy_price,
        total_value: total_value,
    }

    let xhr = get_json_ajax("PUT", '/inventory/row');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#inventory_table').DataTable().ajax.reload();
                get_total();
        }
    }

    xhr.send(JSON.stringify(data));
}

function add_row(){
    let part_code = document.getElementById("inventory_part_code").value;
    let description = document.getElementById("inventory_description").value;
    let producer = document.getElementById("inventory_producer").value;
    let quantity_str = document.getElementById("inventory_quantity").value;
    let catalog_price_str = document.getElementById("inventory_catalog_price").value;
    let discount_str = document.getElementById("inventory_discount").value;

    let quantity = parseInt(quantity_str);
    let catalog_price = parseFloat(catalog_price_str);
    let discount = parseFloat(discount_str);

    let buy_price = catalog_price * (1 - discount/100);
    let total_value = buy_price * quantity;

    let data = {
        part_code : part_code,
        description : description,
        producer : producer,
        quantity : quantity,
        catalog_price : catalog_price,
        discount : discount,
        buy_price: buy_price,
        total_value: total_value,
    }

    let xhr = get_json_ajax("POST", '/inventory/row');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#inventory_table').DataTable().ajax.reload();
                get_total();
        }
    }

    xhr.send(JSON.stringify(data));
    document.getElementById("inventory_part_code").value = "";
    document.getElementById("inventory_description").value = "";
    document.getElementById("inventory_producer").value = "";
    document.getElementById("inventory_quantity").value = "";
    document.getElementById("inventory_catalog_price").value = "";
    document.getElementById("inventory_discount").value = "";
}

function add_to_rent()
{
    let part_code = document.getElementById("inventory_rent_part_code").value;
    let description = document.getElementById("inventory_rent_description").value;
    let quantity = document.getElementById("inventory_rent_quantity").value;
    let position = document.getElementById("inventory_rent_position").value;
    let rent_date = document.getElementById("inventory_rent_rent_date").value;

    let data = {
        part_code: part_code,
        description: description,
        quantity: quantity,
        position: position,
        rent_date: rent_date
    }

    let xhr = get_json_ajax("POST", '/rents/row');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#rents_table').DataTable().ajax.reload();
        }
    }

    xhr.send(JSON.stringify(data));
    document.getElementById("inventory_rent_part_code").value = "";
    document.getElementById("inventory_rent_description").value = "";
    document.getElementById("inventory_rent_quantity").value = "";
    document.getElementById("inventory_rent_position").value = "";
    document.getElementById("inventory_rent_rent_date").value = "";
}

function get_total(){
    let xhr = get_json_ajax("GET", '/inventory/total');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
          document.getElementById("catalog_total_value").value = JSON.parse(this.response)['catalog_total'].toLocaleString('it-IT', { style: 'currency', currency: 'EUR' });
          document.getElementById("inventory_total_value").value = JSON.parse(this.response)['buy_total'].toLocaleString('it-IT', { style: 'currency', currency: 'EUR' });
          document.getElementById("total_marginality").value = JSON.parse(this.response)['marginality'].toLocaleString('it-IT', { style: 'currency', currency: 'EUR' });
        }
    }

    xhr.send(JSON.stringify({}));
}

