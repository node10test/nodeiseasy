$(document).ready(function () {
        const id = 4;
        $.ajax({
            type: "GET",
            url: `/users/${id}`,
            data: {},
            success: function (response) {
                const rows = response["users"]
                let name = rows['name']
                let desc = rows["desc"]
                // console.log(name)
                // console.log(desc)
                let temp_html = `<form method="post" action="/users/${id}">
                                    <div class="whole">
                                        <div class="myprofile">
                                            <div class="myphoto">
                                                <input id="file" type="file" name="file">
                                                <button id="file-btn"><input type="submit" value="저장" class="btn btn-default"></button>
<!--                                                <img src="../images/profile.jpg" style="margin-left: 12rem; margin-bottom: 2rem; border: solid 1px black;" alt="user-image">-->
                                            </div>
                                        </div>
                                        <div class="d1">
                                            <div class="a1">아이디</div>
                                            <div class="form-floating mb-3" style="flex-grow: 2; ">
                                                <input type="name" class="form-control" id="name" name="name" placeholder="${name}">
                                            </div>
                                        </div>
                                        <div class="d2">
                                            <div class="a2">소개</div>
                                            <div class="form-floating mb-3" style="flex-grow: 2;">
                                                <input type="id" class="form-control" id="id" name="desc" placeholder="${desc}">
                                            </div>
                                        </div>
                                        <a href='/static'>
                                            <button style="margin-left: 15rem"><input type="submit" value="수정하기"></button>
                                        </a>
                                        <a href='/static'>
                                            <button type="button" class="btn btn-dark" style="margin-left: 1rem">닫기</button>
                                        </a>
                                    </div>
                                </form>`
                $('.myinfo').append(temp_html)
            }
        })

        function post_users() {
            let name = $('#name').val();
            let desc = $('#desc').val();
            console.log(name, desc)

            $.ajax({
                type: "POST",
                url: `/users/${id}`,
                data: {name: name, desc: desc},
                success: function (response) {
                    console.log(response['msg']);
                    alert(response['msg']);
                    window.location.href = "/my_page"
                },
            });
        }




 })

// 규렬님 코드
              // $("#btn").click(function () {
        //     const name = $(".name").val();
        //     const desc = $(".desc").val();
        //
        // console.log(name, desc)
        //
        // $.ajax({
        //     type: "PUT",
        //     url: `/users/${id}`,
        //     data: {
        //         give_name: name,
        //         give_desc: desc
        //     },
        // success: function (response) {
        //     console.log(response["msg"]);
        //     alert(response["msg"])
        //     window.location.href = `/users/${id}`;
        //         }
        //     })
        // })
