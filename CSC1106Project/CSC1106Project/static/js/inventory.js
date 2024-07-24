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

function deleteProduct(productID, productName) {
    var deleteConfirmation = confirm(`Are you sure you want to delete this product: ${productName}?`);

    if (deleteConfirmation) {
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: `delete/${productID}`,
            method: 'DELETE',
            headers: { 'X-CSRFToken': csrf_token },
            success: function (response) {
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
    $('#editProductForm').on('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        var formData = new FormData($('#editProductForm')[0]);
        var productId = $('#edit_product_id').val();

        $.ajax({
            url: `update/${productId}`,
            method: "POST",
            data: formData,
            headers: { 'X-CSRFToken': csrf_token },
            processData: false,
            contentType: false,
            success: function (data) {
                if (data.status == 200) {
                    window.location.reload();
                } else if (data.status == 400) {
                    alert('Product not updated successfully');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error: ' + errorThrown);
            }
        });
    });

    $('#submitEditProduct').on('click', function () {
        $('#editProductForm').submit();
    });
});
