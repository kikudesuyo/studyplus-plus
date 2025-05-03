curl -X POST "https://api.studyplus.jp/2/study_records" \
-H "accept: */*" \
-H "accept-encoding: gzip, deflate, br, zstd" \
-H "accept-language: en-US,en;q=0.9" \
-H "authorization: OAuth 66a93eaa-ef8e-48d0-9d60-c87fefa73d5c" \
-H "client-service: Studyplus" \
-H "content-type: application/json; charset=utf-8" \
-H "origin: https://app.studyplus.jp" \
-H "referer: https://app.studyplus.jp/" \
-H "sec-ch-ua: \"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"" \
-H "sec-ch-ua-mobile: ?0" \
-H "sec-ch-ua-platform: \"macOS\"" \
-H "sec-fetch-dest: empty" \
-H "sec-fetch-mode: cors" \
-H "sec-fetch-site: same-site" \
-H "stpl-client-sp2: 1" \
-H "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36" \
-d '{
  "comment": "yamamotos towel and my account is dangerous",
  "duration": 180,
  "material_code": "46bd5511-c7fd-4559-8215-e7221d7e2c9b",
  "post_token": "7160a019-d73b-483b-ad75-3f9e850ea9e6",
  "record_datetime": "2025-05-03T23:31:37.623+09:00",
  "runtimeType": "default",
  "study_source_type": "studyplus"
}' --output response.json --header "Content-Disposition: inline"