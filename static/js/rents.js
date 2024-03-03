function del_row(row_id){
    let xhr = get_json_ajax("DELETE", '/rents/row?row_id=' + row_id);

    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#rents_table').DataTable().ajax.reload();
        }
    }
    xhr.send(JSON.stringify({}));
}

function update_row(){
    let id = document.getElementById("rent_edit_id").value;
    let part_code = document.getElementById("rent_edit_part_code").value;
    let description = document.getElementById("rent_edit_description").value;
    let quantity = document.getElementById("rent_edit_quantity").value;
    let position = document.getElementById("rent_edit_position").value;
    let rent_date = document.getElementById("rent_edit_rent_date").value;

    let data = {
        id: id,
        part_code: part_code,
        description: description,
        quantity: quantity,
        position: position,
        rent_date: rent_date
    }

    let xhr = get_json_ajax("PUT", '/rents/row');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                $('#rents_table').DataTable().ajax.reload();
        }
    }

    xhr.send(JSON.stringify(data));
}

function add_row(){
    let part_code = document.getElementById("rent_add_part_code").value;
    let description = document.getElementById("rent_add_description").value;
    let quantity = document.getElementById("rent_add_quantity").value;
    let position = document.getElementById("rent_add_position").value;
    let rent_date = document.getElementById("rent_add_date").value;

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
    document.getElementById("rent_add_part_code").value = "";
    document.getElementById("rent_add_description").value = "";
    document.getElementById("rent_add_quantity").value = "";
    document.getElementById("rent_add_position").value = "";
    document.getElementById("rent_add_date").value = "";
}
