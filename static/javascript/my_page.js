$(document).ready(function () {
        const id = 4;
        $.ajax({
            type: "GET",
            url: `/users/${id}`,
            data: {},
            success: function (response) {
                const rows = response["users"];
                let name = rows['name']
                let desc = rows["desc"]
                let temp_html = `<div class="myinfo1">
                                      ${name}
                                 </div>
                                 <div class="myinfo2">
                                      ${desc}
                                 </div>
                                <div class="rewrite">
                                    <button type="button" class="btn btn-outline-dark"><a href="/edit">프로필 수정</a></button>                                       
                                </div>`
                $('.myinfo').append(temp_html)
            }
        })
})