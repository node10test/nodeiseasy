        $(document).ready(function () {
            var pageNum = 1;

            $("#search").click(function () {
                $("#bookdiv").html("");

                $.ajax({
                    method: "GET",
                    url: "https://dapi.kakao.com/v3/search/book?target=title",
                    data: { query: $("#query").val(), page: pageNum},
                    headers: {Authorization: "KakaoAK 1348380a99485a963bc8a08535311e97"} // ########부분에 본인의 REST API 키를 넣어주세요.

                })
                .done(function (msg) {
                    console.log(msg);
                    for (var i = 0; i < 10; i++){
                        $("#bookdiv").append("<h2><a href='"+ msg.documents[i].url +"'>" + msg.documents[i].title + "</a></h2>");
                        $("#bookdiv").append("<strong>저자:</strong> " + msg.documents[i].authors + "<br>");
                        $("#bookdiv").append("<strong>출판사:</strong> " + msg.documents[i].publisher + "<br>");
                        $("#bookdiv").append("<strong>요약:</strong> " + msg.documents[i].contents + "...<br>");
                        $("#bookdiv").append("<img src='" + msg.documents[i].thumbnail + "'/><br>");
                    }
                });
            })

            $(window).scroll(function(){

                if ( Math.ceil($(window).scrollTop()) + $(window).height() >= $(document).height() ){
                    pageNum++;


                    $.ajax({
                        method: "GET",
                        url: "https://dapi.kakao.com/v3/search/book?target=title",
                        data: { query: $("#query").val(),  page: pageNum},
                        headers: {Authorization: "KakaoAK 1348380a99485a963bc8a08535311e97"} // ########부분에 본인의 REST API 키를 넣어주세요.

                    })
                    .done(function (msg) {
                        console.log(msg);
                        for (var i = 0; i < 10; i++){
                            $("#bookdiv").append("<h2><a href='"+ msg.documents[i].url +"'>" + msg.documents[i].title + "</a></h2>");
                            $("#bookdiv").append("<strong>저자:</strong> " + msg.documents[i].authors + "<br>");
                            $("#bookdiv").append("<strong>출판사:</strong> " + msg.documents[i].publisher + "<br>");
                            $("#bookdiv").append("<strong>요약:</strong> " + msg.documents[i].contents + "...<br>");
                            $("#bookdiv").append("<img src='" + msg.documents[i].thumbnail + "'/><br>");
                        }
                    });

                }

            });
        })
