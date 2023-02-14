# Location for the new office of our gaming company

For our new company we are looking for the perfect location for our new office.

In our new office we will need space for 87 employees; the employees have reported the following preferences:

- In an area with companies that also do design
- 30% of the company staff have at least 1 child, so schools should be close by.
- The executives want a starbucks close
- Account managers need to travel a lot; easy transport to the airport is important.
- Everyone in the company is between 25 and 40; they like to party.
- The CEO is vegan; some vegan restaurants close by is a must.
- The maintenance guy likes basketball; a court within 10 km would be nice.
- Dobby the office dog needs a groomer

# 1. Selecting the country

First we used our 'Companies' database in Mongo to filter on companies that also do design; as design is a very broad concept we filtered on companies that use the word 'Design' in their company description. In the chart below you will find a chart of the country with the most companies per country following that requierment. 

![image](https://user-images.githubusercontent.com/121023453/218573495-385f6be2-cdc1-42ae-bbdb-b231c5870abc.png)

As we want a location where the company has potential to grow, we can not just decide on the graph above but we should take more factors in consideration such as the country size, the growthrate of the economy and the density. By merging the dataframe we took from Mongo with one we imported and calculating a score, we now have a top 5 of countries with the higest score. 


![image](https://user-images.githubusercontent.com/121023453/218694886-bc9f5b0b-e3df-4c91-af2a-a9528c076bc8.png)

The table above are the coordinates from the 5 companies in Singapore. 

When adding the 5 locations to the map of Signapore, which is divided into districts, we see that a few offices are very close to each other.
The one in district 3 and 4, and the one in district 7 and 8.

For that reason we continue with 3 locations: 1 in district 3, one in district 7 and one in district 20. Those locations are marked with 2 circles, one for a radius of 500m and another one for 1 km

![image](https://user-images.githubusercontent.com/121023453/218574506-c25c31b5-80b2-4ba7-a79d-0f93dec10434.png)

# 2. Preferences of the employees

To consider the preferences of employees, we are looking at the following points:
- Amount of schools within 1km
- Starbucks within 500m
- Clubs within 1km
- Vegan restaurants within 500m
- Basketball courts within 10km
- Groomer within 1km

![image](https://user-images.githubusercontent.com/121023453/218574742-76100493-fa47-404b-93b4-a8d064d8e08e.png)

Here we already see that probably district 7 would be the best district.

When we add markers to the map, we can easily see the distribution of public transport and facilities the employees suggested.

![image](https://user-images.githubusercontent.com/121023453/218575037-c7080da4-9ad5-4571-b39e-3445198dd2fc.png)

# 3. Finding an empty office

Now we have a district that would be the best location for our new office; we need to find an empty office that is big enough for 87 people. To find one, we scraped data from empty offices that are available for rent on '99.co'. As we have a lot of data now, we can compare the average price of offices per district.

![image](https://user-images.githubusercontent.com/121023453/218575274-4b528a2d-69e6-4d1f-a9b8-7dc646d17ea1.png)

The boxplot below shows more information about the price per square feet in District 7

![image](https://user-images.githubusercontent.com/121023453/218575367-1d45b2d0-fd66-4e3e-bae4-76f6059bc3db.png)

Below we see the offices that are available for rent. When checking the map in the .ipynb file; per office it lists the name, the price per month (in S$), square feet and the price per square feet. 

![image](https://user-images.githubusercontent.com/121023453/218693794-f3dd2446-a473-4bd7-8323-ab060d308cc8.png)

From all the offices available, there is only one office available that is suitable for 85 employees:

![image](https://user-images.githubusercontent.com/121023453/218575977-4f9b38f9-e309-489c-95a2-b286906bcf55.png)

Office in Odeon Towers

https://www.99.co/singapore/commercial/rent/property/odeon-towers-office-WKatJHog8GMU2uWcBYzDCb

Coordinates new office: 1.2995192,103.8473046

![image](https://user-images.githubusercontent.com/121023453/218693981-89605b33-9b1e-4322-b21e-6b0e3fcf08bf.png)
