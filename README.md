# cointracker-interview

A Bitcoin Wallet and Transaction Sync Management API

## Assumptions

1. Assumption that auth is something like a JWT that we can derive the user id from
   Because of this I didn't include auth or anything mapping the user to the created wallet or transactions (because that mapping is done via the JWT and auth middleware and then could be used in the code)
2. Assumption that when data is pulled in it is saved raw before running moving through the pipeline (Extract load then transform) ELT instead of (Extract Transform then load) ETL
   Because of this I just saved the results into the "database." Other options (based on a different assumption) could have been to "semi-normalize it" or do some basic indexing, or to completely to the Transform befor the load
3. Assumption that users can add multiple of the same asset of wallet (e.g multiple bitcoin wallets)
   Because of this I added the alias to the wallet so that users (and us) can have a human identifiable way to see the difference between them (besides a uuid)
4. Assumption that if we fail to fetch some of the transactions in a sync that we still want to save the successful one
   This was a big controversial topic at TaxBit when I was there without either side winning. For the sake of time and this demo project I assumed that we wanted to save any successful ones even if some failed (but have a way to know if everything succeeded or not)

## Architecture Decisions

Summary:
The only constant is change rings true almost everywhere, but ESPECIALLY in crypto data. Because of this the focus of my design was on quality,resiliancy and adaptability (open close principal). Whether our data sources for crypto transactions changes or is down, we can easily implement a new provider. If we change databases to better support the new shapes of our data, the switch (on the code level) is a simple swap.

### Clean architecture:

api/controllers => set up service instances and inject them into use cases
usecases => validate data models and execute business logic with injected services

Pros: Adaptable to future changes with limited impact to the code, easy to inject services into tests, potential for dynamic dependency injection

### Syncing:

1. Rate limits are all over the place across different data providers, we need rate limit backoff in the sync: I added that
2. Because of Rate limits and sometimes failed single responses from data providers (many of them are startups) we need retry logic built in to our sync calls: I added that
3. When new users join we need to sync there entire history, but after they have synced there history we only want to sync new transactions (assumption) we need a way to specify a starting point for the sync so that we can sync as many or as few transactions as we want: I added that
4. Because this is a server we don't want to pull all transactions down before saving them because that removes high volume clients/enterprise clients as potential customers, We need to save as we go (or send to etl pipeline as we go): I added that

## Environment Setup

1. Install Python (3.9.15) https://realpython.com/installing-python/
2. Optional: Install Postman for easier api calls

3. In the project directory: install dependencies `pip install -r requirements.txt`

## Running the server

`python app.py` (this runs on port 5001, if you would like to change this modify it in app.py)

## View the docs

In a browser go to `http://127.0.0.1:<YOUR SERVER PORT HERE>/` and you will see swagger docs on what endpoints are available and the request bodies required for the POST endpoints

## Suggestion API Interaction

Included in the repository is a postman collection:
<br>
`CoinTracker.postman_collection.json`
<br>
The recommended/preffered way to call the api is to import the collection into postman and make calls from there. Other API calling methods are acceptable.

## Future Improvements and Plans

This was a fun project and could go so many different places, had I had more time and been working on this like a real projcet the next steps would be:

### Testing - The following tests would be added:

Add Wallets:

<ol type="a">
   <li> Test for succesfully adding a new non duplicated wallet with all fields correct</li>
   <li>Test for successfully adding a new non dulicated wallet with all required fields (missing alias) and check for correct creation and default alias
   <li>Test for request shape validation (should fail with reasons if missing fields, extra fields, or wrong types in fields)
   <li>Test for failure to add if it is a duplicated wallet
   <li>Test for either failure at duplicated alias or successful indexing of duplicated alias (e.g alias-1,-2,-3)
   <li>Test for proper error handling upon failure
<li>Test for duplication protection (a post should not overwrite an existing wallet if it already exists, a put endpoint should be used for that)
</ol>
<br>
Remove Wallets:
<ol type ="a">
   <li>Test for succesfully adding a new non duplicated wallet with all fields correct
   <li>Test for successfully adding a new non dulicated wallet with all required fields (missing alias) and check for correct creation and default alias
   <li>Test for request shape validation (should fail with reasons if missing fields, extra fields, or wrong types in fields)
   <li>Test for duplication protection (a post should not overwrite an existing wallet if it already exists, a put endpoint should be used for that)
   <li>Test for error handling if trying to delete a non existant wallet
   <li>Test for proper error handling upon failure
</ol>
Sync Wallets:
<ol type ="a">
   <li>Test for succesfully syncing a single page of transactions (fetched and saved)
   <li>Test for successfully syncing multiple pages of transactions (fetched and saved)
   <li>Test for succesful sync from a specific staring point
   <li>Test for successfully waiting for a backoff if a 429 is returned
   <li>Test for successful retry if error occurs
   <li>Test for successfully pulling in large number of transactions
   <li>Test that all successful transactions get saved even if one of the paginations fails
</ol>
Wallet Balance:
<ol type ="a">
   <li>Test for succesfully fetching a balance
   <li>Test for successfully conversion between "raw balance" and "normalized balance"
   <li>Test for succesful handling of a failed provider call
   <li>Test for successful handling of a bad wallet address
</ol>
Wallet Transactions:
<ol type ="a">
   <li>Test for succesfully fetching a single page of transactions default page size(fetched and saved)
   <li>Test for successfully fetching a single page with custom page size
   <li>Test for not allowing a page 0/defaulting 0 to 1
   <li>Test for not allowing pageSize greater than 50 and defaulting to 50 if it is greater
</ol>

### Other TODO's

All the TODO's that I marked while working on the code

<ol>
<li>TODO Break the models into their own directory
<li>TODO : Add Authentication so user can only add/access theirs + correct organization in db
<li>TODO : Add Validation
<li>TODO : Add Validation
<li>TODO : add a Get to get a specific wallet by address
<li>TODO : Make this kick off an async process and return
<li>TODO : make the chain service be based on the chain type
<li>TODO : we could do a summary endpoint that returns balance and last n number of transactions
<li>TODO : make the chain service be based on the chain type
<li>TODO : Move page and pageSize to consts
<li>TODO : make the chain service be based on the chain type
<li>TODO : Look into ccxt blockchains options
<li>TODO : Use validated response models
<li>TODO : Look into ccxt blockchains options
<li>TODO : JWT for user id
<li>TODO add validation that the alias doesn't get duplicated
<li>TODO put all error messages in a const file and better Error handling
<li>TODO Get DB_URL from config
<li>TODO : Decouple fetch and save
<li>TODO : Dockerize the app for easy deployment
</ol>
