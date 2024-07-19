function getNecessaryInformationToPopulate(){
  populateProductDetails();
  populateInventorySummary();
  populateTopSellingItems();
  populateTopSalesPerMonth();
}

function populateProductDetails(){

  $.ajax({
    url: "get_product_details/",
    type: "GET",
    success: function(data){
      for (const [key,value] of Object.entries(data)){
        indexKey = `#${key}`
        $(indexKey).html(value);
      }
    }
  })
}

function populateInventorySummary(){
  $.ajax({
    url: "inventory_summary/",
    type: "GET",
    success: function(data){
      for (const [key,value] of Object.entries(data)){
        indexKey = `#${key}`
        $(indexKey).html(value.total_quantity);
      }
    }
  })

}


function populateTopSellingItems(){


}


function populateTopSalesPerMonth(){
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '$Sales per month',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });


}


$(document).ready(function(){

  getNecessaryInformationToPopulate(); 

  setInterval(function(){getNecessaryInformationToPopulate()},30000)


});
