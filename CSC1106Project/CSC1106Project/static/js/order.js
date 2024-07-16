function openEditViewModal(orderId){
    $('#order_id').val(orderId);
    $('#orderEditModal').modal('show');
}


$(document).ready(function() {

    $('#orderForm').on('submit',function(event){
        event.preventDefault();
        var csrftoken = $('input[name=csrfmiddlewaretoken').val()
        var formData = $(this).serialize();
        
        $.ajax({
            url: 'create',
            method: 'POST',
            data: formData ,
            headers : {'X-CSRFToken': csrftoken},
            success: function(data) {
                if (data.status == 200){
                    alert(data.message);
                    window.location.reload();
                }else{
                    alert(data.message);
                }

            }, error: function(jqXHR, textStatus, errorThrown) {
                alert("Some Error occured", errorThrown);

            }
        });
    });

    $('#submitItem').on('click',function(){
        $('#orderForm').submit();
    });

    
    $('#editSubmitBtn').on('click',function(){
        $('#editOrderForm').submit();
    });


    $('#editOrderForm').on('submit',function(event){
        event.preventDefault();
        var csrftoken = $('input[name=csrfmiddlewaretoken').val()
        var formData = $(this).serialize();
        var orderId = $('#order_id').val();

        $.ajax({
            url: `edit/${orderId}`,
            method:'POST',
            data: formData,
            headers : {'X-CSRFToken': csrftoken},
            success: function(data) {
                if (data.status == 200){
                    alert(data.message);
                    location.replace('http://127.0.0.1:8000/inventory/management');
                }else{
                    alert(data.message);
                }

            }, error: function(jqXHR, textStatus, errorThrown) {
                alert("Some Error occured", errorThrown);

            }
        })
    });

    
}); 


