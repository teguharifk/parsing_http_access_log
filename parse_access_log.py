import re
from datetime import date, timedelta

def AccessLogExtract(date):
    logFilePath = r'/Users/teguh/Development/log/damer_dashboard/access_log.log'
    timeStampRgx = '\[('+date+'.*?)\]'
    IPRgx = '((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))'
    quoteRgx = '"(.*?)"'
    IPList = []
    TimeList = []
    browserList = []
    statusCodeList = []
    with open(logFilePath, "r") as file:
        for line in file:
            cleanBrowser = re.sub(quoteRgx, '', line)
            cleanIP = re.sub(IPRgx, '', cleanBrowser)
            statusCode = re.sub(timeStampRgx, '', cleanIP).replace('-', '').replace(' ', '')[0:3]
            statusCodeList.append(statusCode)
            browserSingle = []
            for timeMatch in re.finditer(timeStampRgx, line, re.S):
                match_text = timeMatch.group()
                TimeList.append(match_text[1:-7])
            for ipMatch in re.finditer(IPRgx, line, re.S):
                match_text = ipMatch.group()
                IPList.append(match_text)
            for quoteMatch in re.finditer(quoteRgx, line, re.S):
                match_text = quoteMatch.group()
                browserSingle.append(match_text)
            browserList.append(browserSingle)
    file.close()
    accessLogList = list(zip(TimeList, IPList, statusCodeList, browserList))
    return accessLogList

if __name__ == '__main__':
    today = (date.today() - timedelta(days=1)).strftime("%d/%b/%Y")
    datas = AccessLogExtract(today)
    for data in datas:
      print(data)


