require 'csv'

class ManifestParser
  def initialize(fpath, coldict, default)
    @reader = CSV.read(

  end


end

CSV.foreach("test.csv") do |row|
  
end
