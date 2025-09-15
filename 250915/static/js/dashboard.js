/* globals Chart:false */

(() => {
  'use strict'

  // Graphs
  // 문서 안에 있는 ID가 myChart인 태그를 선택하여 ctx 변수에 저장
  const ctx = document.getElementById('myChart')
  // ctx에 그래프를 그려준다.
  new Chart(ctx, {
    // 어떤 그래프를 그릴것인가?
    type: 'bar',
    data: {
      // x축의 데이터를 대입 
      labels: {{x | tojson}},
      // y축의 데이터를 대입( 복수 y 축 데이터 가능 )
      datasets: [
        {
          // 실제 y축 데이터가 대입되는 부분
          data: {{y | tojson}},
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  })
})()
