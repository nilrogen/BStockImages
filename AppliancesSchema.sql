USE BStock;

DROP TABLE IF EXISTS ItemDescription;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Marketplace;
DROP VIEW IF EXISTS WhirlpoolView;
DROP VIEW IF EXISTS LowesView;
DROP VIEW IF EXISTS AlmoView;

CREATE TABLE Item (
   ModelNumber        VARCHAR(100) NOT NULL,
   bstockCategory     VARCHAR(100), 
   bstockSubcategory  VARCHAR(100), 
   brand              VARCHAR(50), 
   MSRP               DECIMAL(7,2),
   MAP                DECIMAL(7,2),
   Weight             FLOAT,
   ShipWeight         FLOAT,
   ImageLocation      VARCHAR(100),
   ImageMime          VARCHAR(5),
   PRIMARY KEY(Modelnumber)
);

INSERT INTO Item
VALUES ("test", "TestCat", "TestSubCat", "TestBrand", 123, 123, 10, 10, "test.jpg", "jpg");

CREATE TABLE Marketplace (
   idMarketplace   INT NOT NULL AUTO_INCREMENT, 
   mktpName        VARCHAR(50),
   manufacturer    BOOLEAN DEFAULT FALSE,
   website 		   VARCHAR(255),
   PRIMARY KEY (idMarketplace, mktpName)
);

CREATE TABLE ItemDescription (
   ModelNumber     VARCHAR(100),
   idMarketplace   INT NOT NULL,
   SKU             VARCHAR(50), 
   UPC             INT(12),
   Description     VARCHAR(255), 
   RetailPrice     DECIMAL(6,2),
   mktCategory     VARCHAR(100),
   mktSubcategory  VARCHAR(100),
   FOREIGN KEY (Modelnumber) 
     REFERENCES Item(Modelnumber),
   FOREIGN KEY (idMarketplace)
     REFERENCES Marketplace(idMarketplace)
);

CREATE VIEW WhirlpoolView AS
SELECT i.Modelnumber, brand, MSRP, MAP, Weight, ShipWeight, 
	   id.idMarketplace, SKU, UPC, Description, RetailPrice, mktCategory, mktSubcategory
FROM Item i 
   JOIN ItemDescription id ON i.Modelnumber LIKE id.ModelNumber
WHERE id.idMarketplace = 1;

CREATE VIEW LowesView AS
SELECT i.Modelnumber, brand, MSRP, MAP, Weight, ShipWeight, 
	   id.idMarketplace, SKU, UPC, Description, RetailPrice, mktCategory, mktSubcategory
FROM Item i 
   JOIN ItemDescription id ON i.Modelnumber LIKE id.ModelNumber
WHERE id.idMarketplace = 4;

CREATE VIEW AlmoView AS
SELECT i.Modelnumber, brand, MSRP, Weight, ShipWeight,
	   Description, mktCategory, mktSubcategory
FROM Item i 
   JOIN ItemDescription id ON i.Modelnumber LIKE id.ModelNumber
WHERE id.idMarketplace = 4;
        
INSERT INTO Marketplace (mktpName, manufacturer, website)
VALUES ("Whirlpool", TRUE, "www.whirlpool.com");

INSERT INTO Marketplace (mktpName, website)
VALUES ("Bestbuy", "www.bestbuy.com");

INSERT INTO Marketplace (mktpName, manufacturer, website)
VALUES ("Frigidaire", TRUE, "www.frigidaire.com");

INSERT INTO marketplace (mktpName, website)
VALUES ("Lowes", "www.lowes.com");
