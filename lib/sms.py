import MySQLdb

sql = """select ID, count(1) as NumParts, SenderNumber, max(ReceivingDateTime) as Timestamp,
  if(LENGTH(UDH) = 0, ID, substr(UDH, 1, Length(UDH)-2)) as MultipartId,
  group_concat(TextDecoded) as Text
from inbox
group by SenderNumber, MultipartId
order by ReceivingDateTime desc
limit 1;""";

db = MySQLdb.connect(host = "localhost", user = "sms", passwd = "sms", db = "sms")

def get_last():
  cur = db.cursor()
  cur.execute()
  result = cur.fetchone()
  return result
