$(function() {
  $(".search_button").click(function() {
      var search_word = $("#search_box").val();
      var dataString = 'search_word='+ search_word;
      if(search_word==''){
      }else{
        $.ajax({
          type: "GET",
          url: `/searchdata?search_word=${search_word}`,
          // data: dataString,
          cache: false,
          beforeSend: function(html) {
              document.getElementById("insert_search").innerHTML = '';
              $("#flash").show();
              $("#searchword").show();
              $(".searchword").html(search_word);
              $("#flash").html('<img src="/static/image/loader.gif" align="absmiddle"> Loading Results...');
            },
          success: function(html){
              $("#insert_search").show();
              $("#insert_search").append(html.data);
              $("#flash").hide();
          }
        });
      }
    return false;
  });
});