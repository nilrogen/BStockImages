require 'csv'

class ManifestParser
  def initialize(fpath, coldict, default)
    @reader = CSV.new(fpath, :headers=>true)
  end
end 
