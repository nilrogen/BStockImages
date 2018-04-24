require "nokogiri"
require "open-uri"
require "json"

page = Nokogiri::HTML(open("https://www.homedepot.com/s/206374433"))


scripts = page.search("script")
scripts.each { |value|
  mtch = /BREADCRUMB_JSON = ({.*?});/.match(value)
  if mtch != nil
    values = JSON.parse(mtch[1])
    values = values["bcEnsightenData"]["contentSubCategory"]
    values.split(">")
  end
}


