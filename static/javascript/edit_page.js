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
            let temp_html = `<form method="post" action="/users/${id}" >
                                    <div class="whole">
                                        <div class="myprofile">
                                           <form method="post" action="/upload" enctype="multipart/form-data" class="form-inline">
                                                <div class="form-group">
                                                    <label>Choose Images: </label>
                                                    <input type="file" name="files[]" id="fileInput" onchange="test()" class="form-control" multiple>
                                                    <img src="" id="ex">
                                                </div>
                                                <input type="submit" name="submit" class="btn btn-success" value="UPLOAD"/>
                                           </form>
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



})

$(document).ready(function () {
        // File type validation
        $("#fileInput").change(function () {
            let fileLength = this.files.length;
            let match = ["image/jpeg", "image/png", "image/jpg", "image/gif"];
            let i;
            for (i = 0; i < fileLength; i++) {
                let file = this.files[i];
                let imagefile = file.type;
                if (!((imagefile == match[0]) || (imagefile == match[1]) || (imagefile == match[2]) || (imagefile == match[3]))) {
                    alert('Please select a valid image file (JPEG/JPG/PNG/GIF).');
                    $("#fileInput").val('');
                    console.log(fileLength)
                    window.location.href = "/"
                    return false;

                }
            }
        });
    })

