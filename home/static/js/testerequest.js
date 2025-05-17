// fetch("https://mexchange-api.bolsadeaposta.bet.br/api/offers", {
//     "headers": {
//       "accept": "application/json",
//       "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
//       "content-type": "application/json",
//       "priority": "u=1, i",
//       "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
//       "sec-ch-ua-mobile": "?0",
//       "sec-ch-ua-platform": "\"Windows\"",
//       "sec-fetch-dest": "empty",
//       "sec-fetch-mode": "cors",
//       "sec-fetch-site": "same-site",
//       "cookie": "BIAB_LANGUAGE=PT_BR; BIAB_TZ=180; BIAB_CURRENCY=BRL; C_U_I=173565; BIAB_CUSTOMER=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJZYWdvRnJlaXJlIiwiZXhwIjoxNzQ2OTEwODUzLCJsb2dpbiI6IllhZ29GcmVpcmUiLCJkb21haW5OYW1lIjoiQk9MU0FERUFQT1NUQSIsInVzZXJfcm9sZSI6Ik1lbWJlciIsInVzZXJJZCI6MTczNTY1LCJsb2dpbklkIjozMDQ1NjU5MCwicGFyZW50RnJvbnRFbmREb21haW4iOiIiLCJ1bmlxdWUiOiJEQ0JmdXRsSCJ9.GksAboGVSrXBFurBaOwmyceJBlUDw7tY-Qdr4Ikd6c8f3JI5vKAdXHeB9xC-auEPUvEBrZMlE-HaCXYxfAa3CQ; sb=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJZYWdvRnJlaXJlIiwiZXhwIjoxNzQ2OTEwODUzLCJsb2dpbiI6IllhZ29GcmVpcmUiLCJkb21haW5OYW1lIjoiQk9MU0FERUFQT1NUQSIsInVzZXJfcm9sZSI6Ik1lbWJlciIsInVzZXJJZCI6MTczNTY1LCJsb2dpbklkIjozMDQ1NjU5MCwicGFyZW50RnJvbnRFbmREb21haW4iOiIiLCJ1bmlxdWUiOiJEQ0JmdXRsSCJ9.GksAboGVSrXBFurBaOwmyceJBlUDw7tY-Qdr4Ikd6c8f3JI5vKAdXHeB9xC-auEPUvEBrZMlE-HaCXYxfAa3CQ",
//       "Referer": "https://mexchange.bolsadeaposta.bet.br/",
//       "Referrer-Policy": "strict-origin-when-cross-origin"
//     },
//     "body": "{\"odds-type\":\"DECIMAL\",\"exchange-type\":\"back-lay\",\"offers\":[{\"runner-id\":\"29983450740700076\",\"event-id\":\"29983419799500076\",\"market-id\":\"29983450740000076\",\"side\":\"back\",\"odds\":1.48,\"stake\":1,\"keep-in-play\":false}]}",
//     "method": "POST"
//   });

// fetch("https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplay-info", {
//   "headers": {
//     "accept": "application/json",
//     "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
//     "priority": "u=1, i",
//     "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
//     "sec-ch-ua-mobile": "?0",
//     "sec-ch-ua-platform": "\"Windows\"",
//     "sec-fetch-dest": "empty",
//     "sec-fetch-mode": "cors",
//     "sec-fetch-site": "same-site"
//   },
//   "referrer": "https://mexchange.bolsadeaposta.bet.br/",
//   "referrerPolicy": "strict-origin-when-cross-origin",
//   "body": null,
//   "method": "GET",
//   "mode": "cors",
//   "credentials": "include"
// });

const xsrfToken = "eyJpdiI6IkdrQ1dkMzdiZ3RoaG42TjFiOTFmTFE9PSIsInZhbHVlIjoiMHdqSE5XOFpacFY4cXJxbzlVcHE4STNFbWpCQzBpcGloS2IxaVFsb0RtcmwwZmxxRkJYcEEwNGttWDFLeWlMdmRwdCtVSTJQNkMwRzFJQzJMWHlUUlYra3JvSWRRYy9ZN082SWF0bXVMOUthVnV6ZThKVWV2VTQ5d0psUi80aTMiLCJtYWMiOiIzYWQ4N2ZjZmMwZDg1MzJhYzE5MzJhMjQ2MjdlOWM3MzQ1MTcxZWU2NWIzNWI5YWZlNDEyMjU2OWRkYmY2ZjY5IiwidGFnIjoiIn0%3D"
const radar = "eyJpdiI6Ik5HaFluK1Z3WDNPSFdHODRtVXZYNEE9PSIsInZhbHVlIjoiOVVNWG5PR1dHUm0vR2JEKytoWi9peUN5VDhDdDZtMTc4MXRObi95ZG9aWGlxRWlQd2FDSUttNU9BUStYaUFVbUxScGVmM201bHNSWjYxSGJnRDZSS0xpeDFxN3B2bzRURFhOTUlxRGZIWlJtdUFDWjNwSnNEdGhNTFBRZlZFTHQiLCJtYWMiOiJiZGViNjdlNDdmM2MwZTMzMjY2MjhkZmEwZjllYTczYzU0ZGRlMjY0NDBhMDE2NTdiNjFkOWUwMTgxOWY1MzVmIiwidGFnIjoiIn0%3D"
const jogos = "eyJpdiI6IkdCcGRJdGk1SE55MEhERG9yOGF1Z2c9PSIsInZhbHVlIjoiNC9oaEU4dmR6N3RoNWJlNExPKzVCcGY4NEhRMkRBckJ2eGdVZ25mVVMydFU0TUpMN2lhb1pqZzZKOU9hRmQyRSIsIm1hYyI6IjNiOTU1OTFhOTY1NWJkNGE2MTAwODBjOWJhNzg4Y2JhNjIxNmRiZDliNjQxYjg1OWJiYWRmODY3MTdlY2RkMmUiLCJ0YWciOiIifQ%3D%3D"
const idioma = "eyJpdiI6ImltdFIrUHh4RWs2Tmw2dGs5eUZqdkE9PSIsInZhbHVlIjoiSlE4cUtJM3RWK09kTWJ1aFNHZFZIMW96amJ4aWdqeXU5Mk53SmsvQUdhRnJ3K0hFcVJlei9LQ0dic2twZ1dXRyIsIm1hYyI6IjYzMjdlMDQ0MDAxYzU2MjMxMjFlYjE3NDhmYzU1OGRiMTI0Njc2MTkxMDlkOGUyZjFmYTJiZDk4MGY3ZTM0OWEiLCJ0YWciOiIifQ%3D%3D"
const fuso = "eyJpdiI6IlFxNTlIc3ltSUUxYi9jNW1qRDc3OGc9PSIsInZhbHVlIjoiWlhlOStlaG1QUHdCQTFraHpZNDN5Nkd5RUxLMlBXNmRzYXVvLzNGclNBT3A1aUN0SlJjdHAvR2pUanlJd1BNNyIsIm1hYyI6ImQ2YjNlMzUwZDRiZTBjYTg5YzYxZjRjMjAyNDBkNTZiYTY2NDg5NDg1Njc3NmZiNmFlNjE3NjM1MmNiMDA4NTUiLCJ0YWciOiIifQ%3D%3D"
const dark = "eyJpdiI6ImlxT3d2b0VsL212TWhCWEdNbnBUYkE9PSIsInZhbHVlIjoiVXVRMTVIQTFpbmQrZE5sbVhjdVpSRWtYWHNETTRVbll6dS9sUHE4TThPWU4rVndvOUtuZEFaaVdiZ1M4YmNxYSIsIm1hYyI6ImFlMmY2NTZjZjQ4OGVlMTAwYTgwNTE3OWY2NTJhNWJhOGIyYjJjYTBjMDNlZGRmOTFmYzJkMjBmYjBhMjVhNTgiLCJ0YWciOiIifQ%3D%3D"

let data = {"fingerprint":{"id":"FkymMEjmod2NvRwHgNWu","name":"ladder","locale":"pt-br","path":"ladder","method":"GET","v":"acj"},"serverMemo":{"children":[],"errors":[],"htmlHash":"637313cc","data":{"indice":0,"odds":["1000","990","980","970","960","950","940","930","920","910","900","890","880","870","860","850","840","830","820","810","800","790","780","770","760","750","740","730","720","710","700","690","680","670","660","650","640","630","620","610","600","590","580","570","560","550","540","530","520","510","500","490","480","470","460","450","440","430","420","410","400","390","380","370","360","350","340","330","320","310","300","290","280","270","260","250","240","230","220","210","200","190","180","170","160","150","140","130","120","110","100","95","90","85","80","75","70","65","60","55","50","48","46","44","42","40","38","36","34","32","30","29","28","27","26","25","24","23","22","21","20","19.5","19.0","18.5","18.0","17.5","17.0","16.5","16.0","15.5","15.0","14.5","14.0","13.5","13.0","12.5","12.0","11.5","11.0","10.5","10.0","9.8","9.6","9.4","9.2","9.0","8.8","8.6","8.4","8.2","8.0","7.8","7.6","7.4","7.2","7.0","6.8","6.6","6.4","6.2","6.0","5.9","5.8","5.7","5.6","5.5","5.4","5.3","5.2","5.1","5.0","4.9","4.8","4.7","4.6","4.5","4.4","4.3","4.2","4.1","4.0","3.95","3.90","3.85","3.80","3.75","3.70","3.65","3.60","3.55","3.50","3.45","3.40","3.35","3.30","3.25","3.20","3.15","3.10","3.05","3.00","2.98","2.96","2.94","2.92","2.90","2.88","2.86","2.84","2.82","2.80","2.78","2.76","2.74","2.72","2.70","2.68","2.66","2.64","2.62","2.60","2.58","2.56","2.54","2.52","2.50","2.48","2.46","2.44","2.42","2.40","2.38","2.36","2.34","2.32","2.30","2.28","2.26","2.24","2.22","2.20","2.18","2.16","2.14","2.12","2.10","2.08","2.06","2.04","2.02","2.00","1.99","1.98","1.97","1.96","1.95","1.94","1.93","1.92","1.91","1.90","1.89","1.88","1.87","1.86","1.85","1.84","1.83","1.82","1.81","1.80","1.79","1.78","1.77","1.76","1.75","1.74","1.73","1.72","1.71","1.70","1.69","1.68","1.67","1.66","1.65","1.64","1.63","1.62","1.61","1.60","1.59","1.58","1.57","1.56","1.55","1.54","1.53","1.52","1.51","1.50","1.49","1.48","1.47","1.46","1.45","1.44","1.43","1.42","1.41","1.40","1.39","1.38","1.37","1.36","1.35","1.34","1.33","1.32","1.31","1.30","1.29","1.28","1.27","1.26","1.25","1.24","1.23","1.22","1.21","1.20","1.19","1.18","1.17","1.16","1.15","1.14","1.13","1.12","1.11","1.10","1.09","1.08","1.07","1.06","1.05","1.04","1.03","1.02","1.01"],"tipo":"stake","stake":100,"layVencedor":0,"backVencedor":0,"stakeTotalLay":0,"stakeTotalBack":0,"oddMediaLay":0,"oddMediaBack":0,"plTotalLay":0,"plTotalBack":0,"valores":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"valoresLay":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"valoresBack":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"lays":[],"backs":[]},"dataMeta":[],"checksum":"ff095b7135f859ba074aa84ed241c7e713966d8788d939c5b5e3867423e32bcc"},"updates":[{"type":"callMethod","payload":{"id":"nvd3","method":"adicionarBack","params":[1.16]}}]}
fetch("https://www.radarfutebol.com/livewire/message/ladder", {
  "headers": {
    // "origin": "https://www.radarfutebol.com",
    // "accept": "text/html, application/xhtml+xml",
    // "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    // "accept-encoding": "gzip, deflate, br, zstd",
    "content-type": "application/json",
    "priority": "u=1, i",
    // "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    // "sec-ch-ua-mobile": "?0",
    // "sec-ch-ua-platform": "\"Windows\"",
    // "sec-fetch-dest": "empty",
    // "sec-fetch-mode": "cors",
    // "sec-fetch-site": "same-origin",
    "x-csrf-token": "agzbgO5ZlemZ9OvmtR0AJ5eL1dMhk09hIv9W05tU",
    // "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    // "x-livewire": "true",
    "cookie": `SRVGROUP=common;XSRF-TOKEN=${xsrfToken};radarfutebolcom_session=${radar};dark=${dark};fuso-horario=${fuso};idioma=${idioma};jogos-ordem-inicio=${jogos};`,
    // "Referer": "https://www.radarfutebol.com/ladder",
    // "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "method": "POST",
  "body": JSON.stringify(data)
}).then(response => response.json()).then(data=>{
  console.log(data)
});