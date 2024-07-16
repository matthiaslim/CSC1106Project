function openProductView(productId){
    $.ajax({
        url: `get/${productId}`,
        method: 'GET',
        success: function(data) {
            if (data.status == 200) {
                var product = data.product;
    
                for (var itemName in product) {
                    if (product.hasOwnProperty(itemName)) {
                        var element = document.getElementById(itemName);
                      
                        // Check if element exists before updating
                        if (element) {
                            // Update element content based on its type
                            if (element.tagName.toLowerCase() === 'input' || element.tagName.toLowerCase() === 'textarea' || element.tagName.toLowerCase() === 'select') {
                                element.value = product[itemName];
                            } else if (element.tagName.toLowerCase() === 'img') {
                                element.src = product[itemName];
                            } else {
                                element.textContent = product[itemName];
                            }
                        } 
                    }
                }
                $('#productViewModal').modal('show');   
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Error: ' + errorThrown);
        }
    });

}

function deleteProduct(productID, productName) {
    var deleteConfirmation = confirm(`Are you sure you want to delete this product: ${productName}?`);

    if (deleteConfirmation) {
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url:`delete/${productID}`,
            method: 'DELETE',
            headers: {'X-CSRFToken' : csrf_token},
            success : function (response) {
                if (response.status == 200) {
                    alert("Product deleted successfully.");
                    window.location.reload();
                } else {
                    alert("Product not deleted successfully");
                }
            }
        });
    } 
}

function editProductView(productID){
    $('#edit_product_id').val(productID);
    $('#editProductViewModal').modal('show');   

    
}

function submitEditProduct(){
    
}