USE BStock;

DROP TABLE IF EXISTS ItemDescription;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Marketplace;
DROP VIEW IF EXISTS WhirlpoolView;
DROP VIEW IF EXISTS LowesView;
DROP VIEW IF EXISTS AlmoView;
DROP VIEW IF EXISTS BestBuyView;

CREATE TABLE Item (
   ModelNumber        VARCHAR(20) NOT NULL,
   bstockCategory     VARCHAR(60), 
   bstockSubcategory  VARCHAR(60), 
   brand              VARCHAR(25), 
   MSRP               DECIMAL(7,2),
   MAP                DECIMAL(7,2),
   Weight             FLOAT,
   ShipWeight         FLOAT,
   ImageLocation      VARCHAR(100),
   ImageMime          VARCHAR(5),
   PRIMARY KEY(Modelnumber)
);

CREATE TABLE Marketplace (
   idMarketplace   INT NOT NULL AUTO_INCREMENT, 
   mktpName        VARCHAR(25),
   manufacturer    BOOLEAN DEFAULT FALSE,
   website 		   VARCHAR(50),
   PRIMARY KEY (idMarketplace, mktpName)
);

CREATE TABLE ItemDescription (
   ModelNumber     VARCHAR(20),
   idMarketplace   INT NOT NULL,
   SKU             VARCHAR(50), 
   UPC             INT(12),
   Description     VARCHAR(200), 
   RetailPrice     DECIMAL(7,2),
   mktCategory     VARCHAR(60),
   mktSubcategory  VARCHAR(60),
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

CREATE VIEW BestBuyView AS
SELECT i.Modelnumber, brand, MSRP, MAP, Weight, ShipWeight, 
	   id.idMarketplace, SKU, UPC, Description, RetailPrice, mktCategory, mktSubcategory
FROM Item i 
   JOIN ItemDescription id ON i.Modelnumber LIKE id.ModelNumber
WHERE id.idMarketplace = 2;

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
WHERE id.idMarketplace = 5;
        
INSERT INTO Marketplace (mktpName, manufacturer, website)
VALUES ("Whirlpool", TRUE, "www.whirlpool.com");

INSERT INTO Marketplace (mktpName, website)
VALUES ("Bestbuy", "www.bestbuy.com");

INSERT INTO Marketplace (mktpName, manufacturer, website)
VALUES ("Frigidaire", TRUE, "www.frigidaire.com");

INSERT INTO marketplace (mktpName, website)
VALUES ("Lowes", "www.lowes.com");

INSERT INTO Marketplace (mktpName, website)
VALUES ("Almo", "www.almo.com");
