from nltk.stem.porter import PorterStemmer
import spacy
from gensim.models.phrases import Phraser, Phrases
import itertools
import numpy as np
nlp = spacy.load('en')

BIGRAM_MODEL_PATH = "../gensim_models/"


stemmer = PorterStemmer()

LAW_COUNT = 705

BIGRAM_MODEL = None

STOP_WORDS = set("""
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at
back be became because become becomes becoming been before beforehand behind
being below beside besides between beyond both bottom but by
call can cannot ca could
did do does doing done down due during
each eight either eleven else elsewhere empty enough even ever every
everyone everything everywhere except
few fifteen fifty first five for former formerly forty four from front full
further
get give go
had has have he hence her here hereafter hereby herein hereupon hers herself
him himself his how however hundred
i if in indeed into is it its itself
keep
last latter latterly least less
just
made make many may me meanwhile might mine more moreover most mostly move much
must my myself
name namely neither never nevertheless next nine no nobody none noone nor not
nothing now nowhere
of off often on once one only onto or other others otherwise our ours ourselves
out over own
part per perhaps please put
quite
rather re really regarding
same say see seem seemed seeming seems serious several she should show side
since six sixty so some somehow someone something sometime sometimes somewhere
still such
take ten than that the their them themselves then thence there thereafter
thereby therefore therein thereupon these they third this those though three
through throughout thru thus to together too top toward towards twelve twenty
two
under until up unless upon us used using
various very very via was we well were what whatever when whence whenever where
whereafter whereas whereby wherein whereupon wherever whether which while
whither who whoever whole whom whose why will with within without would
yet you your yours yourself yourselves

অতএব অথচ অথবা অনুযায়ী অনেক অনেকে অনেকেই অন্তত  অবধি অবশ্য অর্থাৎ অন্য অনুযায়ী অর্ধভাগে
আগামী আগে আগেই আছে আজ আদ্যভাগে আপনার আপনি আবার আমরা আমাকে আমাদের আমার  আমি আর আরও 
ইত্যাদি ইহা 
উচিত উনি উপর উপরে উত্তর
এ এঁদের এঁরা এই এক একই একজন একটা একটি  একবার একে এখন এখনও এখানে এখানেই এটা এসো
এটাই এটি এত এতটাই এতে এদের এবং এবার এমন এমনি এমনকি এর এরা এলো এস এসে 
ঐ 
ও ওঁদের ওঁর ওঁরা ওই ওকে ওখানে ওদের ওর ওরা 
কখনও কত কথা কবে কয়েক  কয়েকটি করছে করছেন করতে  করবে করবেন করলে কয়েক  কয়েকটি করিয়ে করিয়া করায়
করলেন করা করাই করায় করার করি করিতে করিয়া করিয়ে করে করেই করেছিলেন করেছে করেছেন করেন কাউকে 
কাছ কাছে কাজ কাজে কারও কারণ কি কিংবা কিছু কিছুই কিন্তু কী কে কেউ কেউই কেন কোন কোনও কোনো কেমনে কোটি
ক্ষেত্রে খুব 
গিয়ে গিয়েছে গুলি গেছে গেল গেলে গোটা গিয়ে গিয়েছে
চলে চান চায় চেয়ে চায় চেয়ে চার চালু চেষ্টা 
ছাড়া ছাড়াও ছিল ছিলেন ছাড়া ছাড়াও
জন জনকে জনের জন্য জন্যে জানতে জানা জানানো জানায়  জানিয়ে  জানিয়েছে জানায় জাানিয়ে জানিয়েছে
টি 
ঠিক 
তখন তত তথা তবু তবে তা তাঁকে তাঁদের তাঁর তাঁরা তাঁহারা তাই তাও তাকে তাতে তাদের তার তারপর তারা তারই তাহলে তাহা তাহাতে তাহার তিনই 
তিনি তিনিও তুমি তুলে তেমন তো তোমার তুই তোরা তোর তোমাদের তোদের
থাকবে থাকবেন থাকা থাকায় থাকে থাকেন থেকে থেকেই  থেকেও থাকায়
দিকে দিতে দিয়ে দিয়েছে দিয়েছেন দিলেন দিয়ে দু  দুটি  দুটো দেওয়া দেওয়ার দেখতে দেখা দেখে দেন দেয়  দেশের  
দ্বারা দিয়েছে দিয়েছেন দেয় দেওয়া দেওয়ার দিন দুই
ধরা ধরে 
নয় না নাই নাকি নাগাদ নানা নিজে নিজেই নিজেদের নিজের নিতে নিয়ে নিয়ে নেই নেওয়া নেওয়ার নয় নতুন
পক্ষে পর পরে পরেই পরেও পর্যন্ত পাওয়া পারি পারে পারেন পেয়ে প্রতি প্রভৃতি প্রায় পাওয়া পেয়ে প্রায় পাঁচ প্রথম প্রাথমিক
ফলে ফিরে ফের 
বছর বদলে বরং বলতে বলল বললেন বলা বলে বলেছেন বলেন  বসে বহু বা বাদে বার বিনা বিভিন্ন বিশেষ বিষয়টি বেশ ব্যবহার ব্যাপারে বক্তব্য বন বেশি
ভাবে  ভাবেই 
মত মতো মতোই মধ্যভাগে মধ্যে মধ্যেই  মধ্যেও মনে মাত্র মাধ্যমে মানুষ মানুষের মোট মোটেই মোদের মোর 
যখন যত যতটা যথেষ্ট যদি যদিও যা যাঁর যাঁরা যাওয়া  যাওয়ার যাকে যাচ্ছে যাতে যাদের যান যাবে যায় যার  যারা যায় যিনি যে যেখানে যেতে যেন 
যেমন 
রকম রয়েছে রাখা রেখে রয়েছে 
লক্ষ 
শুধু শুরু 
সাধারণ সামনে সঙ্গে সঙ্গেও সব সবার সমস্ত সম্প্রতি সময় সহ সহিত সাথে সুতরাং সে  সেই সেখান সেখানে  সেটা সেটাই সেটাও সেটি স্পষ্ট স্বয়ং 
হইতে হইবে হইয়া হওয়া হওয়ায় হওয়ার হচ্ছে হত হতে হতেই হন হবে হবেন হয় হয়তো হয়নি হয়ে হয়েই হয়েছিল হয়েছে হাজার
হয়েছেন হল হলে হলেই হলেও হলো হিসাবে হিসেবে হৈলে হোক হয় হয়ে হয়েছে হৈতে হইয়া  হয়েছিল হয়েছেন হয়নি হয়েই হয়তো হওয়া হওয়ার হওয়ায়
1 2 3 4  5 6 7 8 9 10
১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ ১০

""".split())