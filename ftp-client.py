from ftplib import FTP

host = "host"
user = "user"
password = "password"

with FTP(host) as ftp:
  ftp.login(user, password)
  print(ftp.getwelcome())

  # Download file
  with open('text.txt', 'wb') as f:
    ftp.retrbinary('RETR' + 'mytext.txt', f.write, 1024)

  # Upload file
  with open('file.txt', 'rb') as f:
    ftp.storbinary("STOR" + 'upload.txt', f)

  # Download file from another directory
  ftp.cwd('anotherdir')
  with open('text2.txt', 'wb') as f:
    ftp.retrbinary('RETR' + 'mytext2.txt', f.write, 1024)

  ftp.quit()