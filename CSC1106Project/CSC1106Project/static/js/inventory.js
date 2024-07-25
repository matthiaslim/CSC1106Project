function openProductView(productId) {
    $.ajax({
        url: `get/${productId}`,
        method: 'GET',
        success: function (data) {
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
        error: function (jqXHR, textStatus, errorThrown) {
            alert('Error: ' + errorThrown);
        }
    });
}

function deleteProductModal(productID,productName){
    $('#deleteProductid').val(productID);
    $('#deleteProductName').text(productName);
    $("#deleteProductViewModal").modal('show');
}


function deleteProduct() {
    var productID = $("#deleteProductid").val();
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: `delete/${productID}`,
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrf_token },
        success: function (response) {
            window.location.reload();
        }
    });
    
}

function editProductView(productID) {

    $('#edit_product_id').val(productID);
    $.ajax({
        url: `get/${productID}`,
        method: 'GET',
        success: function (data) {
            if (data.status == 200) {
                var product = data.product;
                for (var itemName in product) {
                    if (product.hasOwnProperty(itemName)) {
                        var element = document.getElementById("id_" + itemName);
                        if (element) {
                            if (itemName != "product_image") {
                                // Update element content based on its type
                                if (element.tagName.toLowerCase() === 'input' || element.tagName.toLowerCase() === 'textarea' || element.tagName.toLowerCase() === 'select') {
                                    element.value = product[itemName];
                                } else {
                                    element.textContent = product[itemName];
                                }
                            } else {
                                $('#preview_img').attr('src', product[itemName]);
                            }
                        }
                    }
                }
                $('#editProductViewModal').modal('show');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('Error: ' + errorThrown);
        }
    });
}

function validateFileType(input) {
    var fileName = document.getElementById("id_product_image").value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#preview_img').attr('src', e.target.result).width(350).height(350);
            };

            reader.readAsDataURL(input.files[0]);
        }
    } else {
        alert("Only jpg/jpeg and png files are allowed!");
    }
}


    $(document).ready(function () {
        $('#editProductForm').submit(function (event) {
            event.preventDefault(); // Prevent the default form submission

            var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
            var productId = $('#edit_product_id').val();
            var formData = new FormData($('#editProductForm')[0]);

            if (formData.get('product_length') > 0  && formData.get('product_width') > 0 && formData.get('product_height') > 0 && formData.get('product_sale_price') > 0) {
                $.ajax({
                    url: `update/${productId}`,
                    method: "POST",
                    data:formData,
                    headers: { 'X-CSRFToken': csrf_token },
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        if(data.status == 200){
                            window.location.reload();
                        }
                    }
                });

            }
    });



    $("#submitDeleteButton").on("click", function(){
        deleteProduct();
    })

    $('#submitEditProduct').on('click', function (event) {
        $('#editProductForm').submit();
    });
});
