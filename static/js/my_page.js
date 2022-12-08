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
                let temp_html = `<form method="post" action="/" enctype="multipart/form-data"></form>
                                     <div class="myinfo0"></div>
                                     <div class="myinfo1">
                                          ${name}
                                     </div>
                                     <div class="myinfo2">
                                          ${desc}
                                     </div>
                                    <div class="rewrite">
                                        <button type="button" class="btn btn-outline-dark"><a href="/edit_page">프로필 수정</a></button>                                       
                                    </div>`
                $('.myinfo').append(temp_html)
            }
        })
})

