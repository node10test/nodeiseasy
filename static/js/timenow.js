 // 실시간 시계 함수, 각 연월일,시분초를 출력하는 메소드로 구현하였음.
        function setClock(){
            var dateInfo = new Date();
            var hour = modifyNumber(dateInfo.getHours());
            var min = modifyNumber(dateInfo.getMinutes());
            var sec = modifyNumber(dateInfo.getSeconds());
            var year = dateInfo.getFullYear();
            var month = dateInfo.getMonth()+1; //monthIndex를 반환해주기 때문에 1을 더해준다.
            var date = dateInfo.getDate();
            document.getElementById("time").innerHTML = hour + ":" + min  + ":" + sec;
            document.getElementById("date").innerHTML = year + "년 " + month + "월 " + date + "일";
        }
        //시계 함수의 값이 10 미만일경우 0을 붙여 비교적 자연스럽게 출력한다. (안할시 4:2:10과 같은 형태로 출력됨)
        function modifyNumber(time){
            if(parseInt(time)<10){
                return "0"+ time;
            }
            else
                return time;
        }
            window.onload = function(){
                setClock();
                setInterval(setClock,1000); //1초마다 setClock 함수 실행
            }
