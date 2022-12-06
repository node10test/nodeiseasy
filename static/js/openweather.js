        $(document).ready(function () {
            showLocation();
            console.log(data)
        });

//발전사항 : 서울 API만 받아오던것이 사용자의 위치를 기반으로 위도와 경도를 받아온 후
        //          HTML에 위도와 경도(두번째 자리까지), 날짜 아이콘(날짜에 따라 변함), 위치(영어로 소재지 출력),
        //          현재 위치 온도(섭씨로 출력, 화씨는 소숫점 두번째 자리까지(화씨 출력하고싶은 경우 주석을 해제하여 사용), 섭씨는 첫번째 자리까지)
        //현재 위도 경도로 위치잡아주고 기반으로 다른 값 출력
            function showLocation(event) {
              var latitude = event.coords.latitude
              var longitude = event.coords.longitude
              document.querySelector("#latitude").textContent = Math.round(latitude *100) / 100
              document.querySelector("#longitude").textContent = Math.round(longitude *100) / 100

            //위도와 경도를 추가하여 weatherUrl이 바뀌므로 사용자의 지역에 따라 서로 다른 값 출력
            //위도와 경도에 따른 종속변수 #앞의 값에따라 변하는 변수들
              let apiKey = "c9094277ce42cae0392ac8222a2dd1f2"
              let weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude
                            + "&lon=" + longitude
                            + "&appid=" + apiKey;
             //api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
                let options = { method: 'GET' }
              $.ajax(weatherUrl, options).then((response) => {
                  // console.log(response)
                  let icon = response.weather[0].icon
                  let iconUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
                  let img = document.querySelector("#wicon")
                  let name = response.name
                  img.src = iconUrl
                  document.querySelector("#temp").textContent =  /*"(" +*/ Math.round((response.main.temp - 273)*10) / 10 +"도"/*+ ")"*/ //+ (response.main.temp)+"°F"  화씨까지 띄우기  // 현재 온도
                  document.querySelector("#name").textContent = name
                }).catch((error) => {
                  console.log(error)
                })
            }
            //위치정보를 불러올수 없을때에 대한 예외처리
            function showError(event) {
              alert("위치 정보를 얻을 수 없습니다.")
            }

            window.addEventListener('load', () => {
              if(window.navigator.geolocation) {
                 window.navigator.geolocation.getCurrentPosition(showLocation,showError)
              }
            })