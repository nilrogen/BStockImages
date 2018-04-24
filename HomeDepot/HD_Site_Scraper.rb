require "csv"
require "fileutils"
require "nokogiri"
require "open-uri"
require "yaml"

class RetailLoader
  attr_reader :retails

  def initialize
    @retails = load_existing_retails
    @good_upcs = 0
    @bad_upcs = 0
  end

  def load_existing_retails
    if File.exist?(FileHandler::MASTER_NAME)
      YAML.load_file(FileHandler::MASTER_NAME)
    else
      puts "We couldn't find the '#{FileHandler::MASTER_NAME}' file."
      puts "Please place that file in the current directory and run the script again."
      exit
    end
  end

  def load_source_upcs
    filename = File.read(ask_for_source_filename)
    csv = CSV.new(filename, headers: :true)

    upc_header = csv.first.headers.find { |header| header.strip =~ /\Aupc\z|\Asku\z/i }
    upc_header_error unless upc_header

    upcs = csv.each_with_object([]) do |row, results|
      results << row[upc_header]
    end

    upcs.uniq
  end

  def ask_for_source_filename
    loop do
      print "\n\nPlease enter the name of the file you'd like retails pulled for: "
      filename = gets.chomp

      if !filename.match(/\.csv\z/i)
        filename = filename + '.csv'
        if filename.gsub('.csv', '').length == filename.length
          return filename
        else
          puts "The file must be a .csv file.\n\n"
        end
      elsif !File.exist?(filename)
        puts "We couldn't find that file. Please try again.\n\n"
      else
        return filename
      end
    end
  end

  def upc_header_error
    puts "We couldn't find a 'UPC' header in the source file you supplied."
    puts "Please double check the file for the presence of that header/column and run the script again."
    exit
  end

  # 'upcs' is expected to be an array of UPCs.
  def process_upcs(upcs)
    upcs.each_with_index do |upc, index|
      puts "\n\nProcessing UPC #{index + 1} of #{upcs.size}... #{upc}"
      update_retails(upc)
    end
  end

  def update_retails(upc)
    unless @retails[upc] && (Date.today - @retails[upc][:date_pulled]).to_i < 90
      sleep(5)
      scrape_price, scrape_weight, scrape_desc, scrape_brand, scrape_model, scrape_upc = Scraper.scrape(upc)
      scrape_price = scrape_price.to_s.chars.reverse.insert(2, '.').reverse.join('').gsub('$', '').to_f
      scrape_weight = scrape_weight.gsub(',', '').gsub('lb', '').to_s.strip.to_f unless scrape_weight == nil
      scrape_model = scrape_model.gsub('Model # ', '') unless scrape_model == nil
      scrape_upc = scrape_model.to_s.strip unless scrape_upc.nil?
      scrape_url = scrape_url.to_s.strip unless scrape_url.nil?

      if ![0.0, 0, nil, ""].include? scrape_price
        @retails[upc] = { price: scrape_price, weight: scrape_weight, desc: scrape_desc, brand: scrape_brand, model: scrape_model, upc: scrape_upc, url: scrape_url, date_pulled: Date.today }
        @good_upcs += 1
      else
        @bad_upcs += 1
      end
    end
  end

  def report
    puts "\n\nPulled or updated retails for #{@good_upcs} UPCs."
    puts "There were #{@bad_upcs} UPCs that we couldn't find retails for.\n\n"
  end

  def run
    process_upcs(load_source_upcs)
    report
    FileHandler.new(@retails)
  end
end

class FileHandler
  MASTER_NAME = "HD Retails MASTER.yml"
  BACKUP_NAME = "HD Retails Backup #{Time.now.to_s.tr(':', '-')}.yml"
  LOOKUP_NAME = "HD Retails Lookup - #{Time.now.to_i.to_s}.csv"

  def initialize(retails)
    @retails = retails

    handle_files
  end

  def handle_files
    create_backup_file

    begin
      write_to_master_retail_file
    rescue
      master_retail_write_error
      exit
    end

    write_to_lookup_file
    delete_backup_file

    report
  end

  def create_backup_file
    File.open(BACKUP_NAME, "w") { |file| YAML.dump(@retails, file) }
  end

  def delete_backup_file
    File.delete(BACKUP_NAME)
  end

  def write_to_master_retail_file
    File.open("#{MASTER_NAME}", "w") do |file|
      YAML.dump(@retails, file)
    end
  end

  def master_retail_write_error(e)
    puts "Sorry. It looks like something went wrong while trying to write to '#{MASTER_NAME}'."
    puts "Error: #{e}"
    puts "We created a backup file in case '#{MASTER_NAME}' was corrupted. We recommend using that backup file by renaming it to '#{MASTER_NAME}' and running the script again."
  end

  def write_to_lookup_file
    File.open("#{LOOKUP_NAME}", "w") do |file|
      file << "sep=|\n"
      file << "UPC|Retail|Weight|Date Pulled|Desc|Brand|Model|GTIN13|URL\n"
      @retails.each { |upc, data| 
        file << "#{upc}|#{data[:price]}|#{data[:weight]}|#{data[:date_pulled]}|#{data[:desc]}|#{data[:brand]}|#{data[:model]}|#{data[:gtin13]}|#{data[:url]}\n" 
      }
    end
  end

  def report
    puts "Updated '#{MASTER_NAME}'"
    puts "Generated an '#{LOOKUP_NAME}' file.\n\n"
  end
end

class Scraper
  def self.scrape(upc)
    begin
      page = Nokogiri::HTML(open("https://www.homedepot.com/s/#{upc}"))
    rescue Exception => e
      puts e.message
      puts e.backtrace.inspect
      return nil, nil, nil, nil, nil, nil
    end

    begin
      price = page.css("span[id='ajaxPrice']").first.text.strip.delete(",")
      print "\nPrice:\t#{price}\n"
    rescue
      price = nil
    end

    begin
      weight = page.css("div[itemprop='weight']").first.text
      print "\nWeight:\t#{weight}\n"
    rescue
      weight = nil
    end

    begin
      desc = page.css("h1.product-title__title").first.text.strip
      print "\nDesc:\t#{desc}\n"
    rescue
      desc = nil
    end

    begin
      brand = page.css("h2.product-title__brand").first.text.strip
      print "\nBrand:\t#{brand}\n"
    rescue
      brand = nil
    end

    begin
      model = page.css("h2[class='product_details modelNo']").first.text.strip
      print "\nModel:\t#{model}\n"
    rescue
      model = nil
    end

    begin
      gtin13 = page.css("div.product-title").css("upc").text.strip
      print "\nGTIN13:\t#{gtin13}\n"
    rescue
      gtin13 = nil
    end

    cats = page.css("div#breadcrumb")
    puts(cats)

    begin 
      url = page.css("img[id='mainImage']").first['src']
      print "\nURL:\t#{url}\n"
    rescue
      url = nil
    end

    return price, weight, desc, brand, model, gtin13, url
  end
end

Scraper.scrape("206374433")

