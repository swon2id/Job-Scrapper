# flask 프레임워크 import
# instagram과 같은 서비스가 해당 프레임 워크로 구현되었음
# render_template는 사용자가 templates 폴더의 html과 같은 파일에 접근하도록 해줌
# request는 웹서버에 접근하는 행위(request)를 rendering하여 처리 하기 위한 함수?
from flask import Flask, render_template, request, redirect, send_file
from scrapper import scraping_jobs
from exporter import save_to_file
# 앱 이름
app = Flask("Super Scrapper")

# fake DB 생성(dictionary)) 하여 scraping 결과 데이터 저장하여 불러오는 방식으로 사용하기
db = {}

# @는 route()의 매개변수에 해당하는 페이지로 접속할 경우 아래의 함수를 호출
# root 페이지 접속시 실행될 func
@app.route("/")
def home():
  return render_template("index.html")

# <>는 placeholder로 이하 함수에서 해당 인자를 받음
@app.route("/<username>")
def usingPlaceholder(username):
  return f"Hello! Your name is {username}"

# URL에 쿼리스트링(query string)을 사용하는 GET 방식으로 주소자체에서 데이터 접근을 처리
# 주소에서 key인 'word'에 대응하는 arg가 return
# render_template 함수는 다음의 값을 인자로 받는다.
# (전달할 html 문서, 해당 html에 전달할 arg들)
@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = scraping_jobs(word)
      db[word] = jobs
      print(f"Scraping results for {word} stored in db")
  else:
    return redirect("/")
  return render_template(
      "report.html",
      searchingBy = word,
      resultsNumber = len(jobs),
      jobs = jobs
    )


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")


# 서버 실행
app.run(host="0.0.0.0")