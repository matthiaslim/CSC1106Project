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
  const indicator = document.getElementById("indict");
  const main = document.getElementById("main");

  $('#noCarouselItem').show();
  $('#carouselTopSelling').hide();

  var productsHTML = '';
  var indicatorHTML = '';

  $.ajax({
    url: "top_selling_items/",
    type: "GET",
    success: function(data){
        const dataProduct = data['Product'];
        if(dataProduct.length > 0){
          for (var i=0; i<dataProduct.length; i++){
            activeClass = i == 0 ? 'active' : '';
            current = i == 0 ? 'true' : '';

            indicatorHTML += `<button type="button" data-bs-indicator="#carouselTopSelling" 
                            data-bs-slide-to="${i}" class=${activeClass} aria-current=${current} 
                            aria-label="Slide ${i}"></button>`

            productsHTML += `<div class="carousel-item ${activeClass}">
                              <img src="/media/${dataProduct[i].product_image}" class="d-block w-100" style="max-height: 400px" alt="${dataProduct[i].product_name}">
                              <div style="color:black;" class="carousel-caption d-none d-md-block">
                                  <h5>${dataProduct[i].product_name}</h5>
                                  <p>${dataProduct[i].product_description}</p>
                              </div>
                        </div>`



          }
          indicator.innerHTML= indicatorHTML;
          main.innerHTML = productsHTML;

          $('#carouselTopSelling').show();
          $('#noCarouselItem').hide();
      }
    }
  })
}


function populateTopSalesPerMonth(){
  let chartStatus = Chart.getChart("myChart");
  if (chartStatus != undefined) {
    chartStatus.destroy();
  }
  $("#noChartItem").show();
  $('#myChart').hide();

  const ctx = document.getElementById('myChart');
  let labels = [];
  let data = [];

  $.ajax({
    url: "display_chart_information/",
    type: "GET",
    success: function(response){
      labels = response.month;
      data = response.data;
      if (data.length > 0){
          
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [{
                label: '$Sales per month',
                data: data,
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
          
        $('#noChartItem').hide();
        $('#myChart').show();
      }
    }
  });


}


$(document).ready(function(){
  getNecessaryInformationToPopulate(); 
  setInterval(function(){getNecessaryInformationToPopulate()},30000)
});
