 

FLAW 1: SQL Injection (A03:2021 – Injection) 

Link to the repository: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project ] 

Source link: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project/blob/main/reviews/views.py#L21 ] 

Description of the flaw: The first flaw is an SQL Injection in the search function. This happens because the application takes user input from the search bar and inserts it directly into a raw database query using a Python "f-string". 

The code does not validate or sanitize the input. This allows an attacker to manipulate the SQL command. For example, by typing input like ' OR '1'='1, the attacker can alter the query logic. Since "1=1" is always true, the database returns all reviews instead of just the ones matching the search. In a real application, this vulnerability could allow attackers to view sensitive data, modify the database, or even bypass authentication. 

How to fix it: To fix this, we must avoid putting user input directly into the query string. Instead, we should use parameterized queries. 

In Django, when using cursor.execute, we can use the %s placeholder. The user input is then passed as a separate list argument. The database driver handles the input as data, not executable code, which prevents the injection. I have provided the corrected code in the comments of views.py. 

 

 

FLAW 2: Cross-Site Scripting / XSS (A03:2021 – Injection) 

Source link: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project/blob/main/reviews/templates/pages/index.html#L17 ] 

Description of the flaw: The third flaw is Stored Cross-Site Scripting (XSS). This occurs because the application trusts user input too much when displaying reviews. 

Users can write reviews containing HTML or JavaScript. When the application displays these reviews on the homepage, the template uses the |safe filter: {{ review.content|safe }}. This filter tells Django to disable its automatic security escaping and render the content as raw HTML. 

If an attacker submits a review containing a script like <script>alert('Hacked')</script>, the browser will execute it. Every time a visitor opens the homepage, the malicious script runs. Attackers can use this to steal session cookies, redirect users to malicious sites, or perform actions on behalf of the victim. 

How to fix it: Django protects against XSS by default. It automatically escapes special characters (like changing < to &lt;), so browsers treat them as text, not code. 

The vulnerability exists solely because of the |safe filter. The fix is simply to remove |safe from the template. Once removed, Django will sanitize the input, and any script tags will be displayed as harmless text instead of being executed. 

 

FLAW 3: Broken Access Control (A01:2021) 

Source link: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project/blob/main/reviews/views.py#L44  ] 

Description of the flaw: The second flaw is Broken Access Control, often called Insecure Direct Object Reference (IDOR). This issue exists in the "delete review" functionality. 

The deletion URL follows a pattern like /delete/1/, where the number is the ID of the review. The view function currently only checks if the user is logged in (@login_required). It fails to check if the logged-in user is actually the author of the review they are trying to delete. 

This means any logged-in user can delete any review simply by changing the ID number in the browser's address bar. For example, User A can delete User B's review by guessing the ID. This is a critical flaw because users should only have permission to modify or delete their own content. 

How to fix it: The fix involves verifying ownership before processing the deletion. When the server receives a delete request, it must compare the current user (request.user) with the review's author (review.author). 

If they do not match, the server should reject the request and return a 403 Forbidden error. I have implemented this check in the commented-out fix within views.py. 

 

 

FLAW 4: Security Misconfiguration / CSRF (A01:2021) 

Source link: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project/blob/main/reviews/views.py#L28 ] 

Description of the flaw: The fourth flaw is Cross-Site Request Forgery (CSRF). This vulnerability allows an attacker to trick a user into performing unwanted actions on the application. 

In the add_review view, I specifically disabled Django’s protection by using the @csrf_exempt decorator. This means the server does not verify where the request is coming from. 

If a hacker creates a malicious website with a hidden form targeting my application, and a logged-in user visits that site, the browser will automatically send a request to add a review. Because the CSRF check is disabled, the application accepts the request. The user creates a review (or performs other state-changing actions) without knowing it. 

How to fix it: To fix this, we must enable Django's built-in CSRF protection. 

Remove the @csrf_exempt decorator from the view in views.py. 

Ensure the HTML form in add_review.html includes the {% csrf_token %} tag. 

This adds a unique, secret token to the form. The server checks this token with every POST request. If a request comes from an external attacker's site, it will lack the correct token, and Django will block it. 

 

FLAW 5: Unvalidated Redirects (A01:2021) 

Source link: [ https://github.com/k1rtsu/CyberSecurityCourse-final-project/blob/main/reviews/views.py#L53 ]  

Description of the flaw: The final flaw is Unvalidated Redirects, found in the login view. The application uses a URL parameter called next to redirect users after they log in (e.g., /login/?next=/home). 

The code currently takes this next parameter and redirects the user immediately without validation: return redirect(next_page). 

This is dangerous because an attacker can construct a link like /login/?next=http://malicious-site.com. If a user clicks this link and logs in, they are immediately sent to the attacker's website. This is often used in phishing attacks. The fake site might look identical to the real one and ask the user to login again, stealing their credentials. 

How to fix it: We must validate the destination URL before redirecting. We should ensure the redirect target is internal to our application and not an external domain. 

Django provides a utility function for this: url_has_allowed_host_and_scheme. In the commented fix, I use this function to check if the next URL is safe. If the URL is external or suspicious, the application ignores it and redirects the user to the default homepage instead. 

 
