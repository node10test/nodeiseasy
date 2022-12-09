//  html 실행이 되면 준비됐으니까 함수를 실행
// get 방식은 ajax를 하고 , post 방식은 form 형태로 수행
$(document).ready(function () {
    const id = 1;
    $.ajax({
        type: "GET",
        url: `/users/${id}`,
        data: {},
        //response 정체 밝히기
        success: function (response) {
            const rows = response["users"]
            let name = rows['name']
            let desc = rows["desc"]
            let img = rows["img"]
            let temp_html = `<div class="whole">
                                    <div class="myprofile">
<!--  action = 폼을 전송할 서버 쪽 스크립트 파일을 지정 / name = 폼을 식별하기 위한 이름 지정 / method = 폼을 서버에 전송할 http 메소드를 정함  -->
<!--  class = 중복 가능 , id = 중복 불가능 name = 폼 통신을 하기 위한 장치? -->
                                        <form method="post" action="/upload" enctype="multipart/form-data" class="form-inline">
                                            <div class="form-group">
<!--  type = 태그 모양을 변경 / name = 태그 이름 / onchange = 미리보기 함수 / placeholder = 태그 입력 값에 대한 힌트  -->
                                                <input type="file" name="files[]" id="fileInput" onchange="test()" class="form-control">
<!--  이미지 경로를 static 폴더 안의 img 폴더의 변수 선언을 한 값? -->
                                                <img src="/static/img/${img}" class="default_img" id="ex" style="width: 36%; height: 15rem;">
                                            </div>
<!--  submit 버튼을 누르면 에러메시지가 웹 브라우저에 출력  -->
                                            <input type="submit" name="submit" class="btn btn-success" value="UPLOAD"/>
                                        </form>
                                    </div>   
<!--                                    method = post , action = users의 id 컬럼 값-->
                                    <form method="post" action="/users/${id}">     
                                        <div class="d1">
                                            <div class="a1">아이디</div>
                                            <div class="form-floating mb-3" style="flex-grow: 2; ">
                                                <input type="name" class="form-control" id="name" name="name" placeholder="${name}">
                                            </div>
                                        </div>
                                        <div class="d2">
                                            <div class="a2">소개</div>
                                            <div class="form-floating mb-3" style="flex-grow: 2; height: 10rem;">
                                                <input type="id" class="form-control" id="id" name="desc" placeholder="${desc}">
                                            </div>
                                        </div>
                                        <a href='/my_page'>
                                            <button style="margin-left: 15rem"><input type="submit" value="수정하기"></button>
                                        </a>
                                        <a href='/my_page'>
<!--                                        버튼 타입이 버튼일 경우 무반응-->
                                            <button type="button" class="btn btn-dark" style="margin-left: 1rem">닫기</button>
                                        </a>
                                    </form>
                            </div>`
            $('.myinfo').append(temp_html)
        }
    })
})

// $(document).ready(function () {
//         // File type validation
//         $("#fileInput").change(function () {
//             let fileLength = this.files.length;
//             let match = ["image/jpeg", "image/png", "image/jpg", "image/gif"];
//             let i;
//             for (i = 0; i < fileLength; i++) {
//                 let file = this.files[i];
//                 let imagefile = file.type;
//                 if (!((imagefile == match[0]) || (imagefile == match[1]) || (imagefile == match[2]) || (imagefile == match[3]))) {
//                     alert('Please select a valid image file (JPEG/JPG/PNG/GIF).');
//                     $("#fileInput").val('');
//                     console.log(fileLength)
//                     window.location.href = "/my_page"
//                     return false;
//                 }
//             }
//         });
// })

