__author__ = 'demiin'

import  os
import sys
import  datetime

path_pdf_arch = '/mnt/periodic/Вечерний мурманск'
path = path_pdf_arch
path_pdf_file = path_pdf_arch
months = ['январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь']

date_week_ago = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")
outFileName = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y %m %d")
print(date_week_ago)

cur_year = datetime.date.today().year
cur_month_int = datetime.date.today().month
cur_month_str = months[int(cur_month_int) - 1]
cur_day = datetime.date.today().day

path_pdf_arch += '/' + str(cur_year) + ' ВМ/' + cur_month_str + '/Архивы/'
path_pdf_file += '/' + str(cur_year) + ' ВМ/' + str(cur_year) + ' ' + str(cur_month_int) + ' ВМ/'
os.system('mkdir /tmp/pdf')
for dirname, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if (filename.endswith('.rar')):
            path_pdf_file = path + "/" + filename[6:10] + " ВМ/" + filename[6:10] + " " + filename[3:5] + " ВМ/"
            arch = path + "/" + filename[6:10] + " ВМ/Архивы/" + filename
            file_check = filename[6:10] + " " + filename[3:5] + " " + filename[0:2] + " ВМ.pdf"
            path_file_check = path + "/" + filename[6:10] + " ВМ/" + filename[6:10] + " " + filename[3:5] + " ВМ/" + file_check
            if not os.path.isfile(path_file_check):
                print ("not exists: " + path_file_check)
                currentday = datetime.datetime.strptime(filename[0:2] + "." + filename[3:5] + "." + filename[6:10], "%d.%m.%Y")
                minus = currentday - datetime.timedelta(days=7)
                #print (currentday)
                #print (minus)
                #print (datetime.datetime.utcnow() - datetime.timedelta(days=7))
                #print(minus.strftime("%d"))
                #print ((datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%d"))
                if (int(minus.strftime("%d")) < int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%d"))):
                    print ("need")
                    os.system('mkdir "' + path_pdf_file + '"')
                    print ('копирую архив: ' + arch + ' в /tmp/pdf')
                    os.system('rsync --progress "' + arch + '"' + ' /tmp/pdf')
                    os.system('cd /tmp/pdf' ' && unrar x ' + filename)
                    os.system('rm "/tmp/pdf/' + filename + '"')
                    print('собираю все в один файл ' + file_check)
                    os.system('cd /tmp/pdf && gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="' + file_check + '" /tmp/pdf/*.pdf')
                    print('перемещаю в каталог для доступа из интернет: ' + path_pdf_file)
                    os.system('mv "/tmp/pdf/' + file_check + '" "' + path_pdf_file + '"')
                    print('очищаю следы')
                    os.system('cd /tmp/pdf && rm *.pdf')
os.system('rm -fr /tmp/pdf')

#for dir, subshere, filesphere in os.walk(path_pdf_arch):
#    if (dir != '.'):
#        for file in filesphere:
#            if (file == date_week_ago + '.rar'):
#                print ('копирую архив: ' + file + ' в /tmp/' + date_week_ago)
#                os.system('mkdir /tmp/' + date_week_ago)
#                os.system('rsync --progress "' + path_pdf_arch + '"' + file + ' /tmp/' + date_week_ago)
#                os.system('cd /tmp/' + date_week_ago + ' && unrar x ' + file)
#                os.system('rm /tmp/' + date_week_ago + '/' + file)
#                print('собираю все в один файл ' + outFileName + '.pdf')
#                os.system('cd /tmp/' + date_week_ago + ' && gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="' + outFileName + ' ВМ.pdf" /tmp/' + date_week_ago + '/*.pdf')
#                print('перемещаю в каталог для доступа из интернет: ' + path_pdf_file)
#                print('mv "/tmp/' + date_week_ago + '/' + outFileName + ' ВМ.pdf" "' + path_pdf_file + '"')
#                os.system('mv "/tmp/' + date_week_ago + '/' + outFileName + ' ВМ.pdf" "' + path_pdf_file + '"')
#                print('очищаю следы')
#                os.system('cd /tmp && rm -fr ' + date_week_ago)

