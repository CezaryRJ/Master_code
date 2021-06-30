import glob;
import mailbox;


#
# wget -r -l 1 -nH -nd https://ietf.org/mail-archive/text/tsvwg/
#

counts = {"all": 0};
issues = {"all": 0};

for year in range(2001, 2021):
  counts[year] = 0;
  issues[year] = 0;
  for file in glob.glob("{}-*.mailcl".format(year)):
#    print(file);
    mbox = mailbox.mbox(file);
    counts[year] += mbox.__len__();
    for key in mbox.iterkeys():
      try:
        message = mbox[key];
        date = message.get("Date", None);
        if date is None:
          issues[year] += 1;
#          print("message #{}: missing Date: header.".format(key));
#          print(message);
#        else: print(key, date);
      except Exception as error:
        issues[year] += 1;
        print("failed to parse message for key {}:".format(key));
        print(error);
  print("{}: {} messages; {} issues.".format(year, counts[year], issues[year]));
  counts["all"] += counts[year];
  issues["all"] += issues[year];

print("all: {} messages; {} issues.".format(counts["all"], issues["all"]));
