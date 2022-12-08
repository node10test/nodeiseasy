    //pagination-body를 클릭 event가 발생했을 경우 e를 매개변수로 받는다
    document.getElementById("pagination-body").addEventListener('click', function (e) {
        //
        if (e.target.tagName !== 'A') return;
        //preventDefault 란?
// a 태그나 submit 태그는 누르게 되면 href 를 통해 이동하거나 , 창이 새로고침하여 실행됩니다.
// preventDefault 를 통해 이러한 동작을 막아줄 수 있습니다.
// 주로 사용되는 경우는
// 1. a 태그를 눌렀을때도 href 링크로 이동하지 않게 할 경우
// 2. form 안에 submit 역할을 하는 버튼을 눌렀어도 새로 실행하지 않게 하고싶을 경우 (submit은 작동됨)
        e.preventDefault();
        if (e.target.href) {
            const getUrlParams = () => {
                var params = {};
                //이건
                e.target.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
                    function (str, key, value) {
                        params[key] = value;
                    }
                );
                return params;
            }
            params = getUrlParams();
            params.search_word = decodeURI(params.search_word);
            console.log(params)
            const search_word = params.search_word;
            const page = e.target.text;

            $.ajax({
                type: "GET",
                url: `/searchdata?search_word=${search_word}&page=${page}`,
                // data: dataString,
                cache: false,
                beforeSend: function (html) {
                    document.getElementById("insert_search").innerHTML = '';
                    $("#flash").show();
                    $("#searchword").show();
                    $(".searchword").html(search_word);
                    $("#flash").html('<img src="/static/image/loader.gif" align="absmiddle"> Loading Results...');
                },
                success: function (html) {
                    $("#insert_search").show();
                    $("#insert_search").append(html.data);
                    $("#flash").hide();
                }
            });
        }
    })
