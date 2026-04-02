from flask import Flask, render_template, request, redirect, url_for
from database import get_db
import json

app = Flask(__name__)


# -------------------- DASHBOARD --------------------

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as count FROM companies")
    company_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM jobs")
    job_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM applications")
    app_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM contacts")
    contact_count = cursor.fetchone()['count']

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM applications
        GROUP BY status
    """)
    status_counts = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html',
                           company_count=company_count,
                           job_count=job_count,
                           app_count=app_count,
                           contact_count=contact_count,
                           status_counts=status_counts)


# -------------------- COMPANIES --------------------

# READ - List all companies
@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies")
    all_companies = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=all_companies)


# CREATE - Add a new company
@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        sql = """INSERT INTO companies
                 (company_name, industry, website, city, state, notes)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['company_name'],
            request.form['industry'],
            request.form['website'],
            request.form['city'],
            request.form['state'],
            request.form['notes']
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('companies'))
    return render_template('add_company.html')


# UPDATE - Edit an existing company
@app.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """UPDATE companies SET
                 company_name=%s, industry=%s, website=%s,
                 city=%s, state=%s, notes=%s
                 WHERE company_id=%s"""
        values = (
            request.form['company_name'],
            request.form['industry'],
            request.form['website'],
            request.form['city'],
            request.form['state'],
            request.form['notes'],
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('companies'))
    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (id,))
    company = cursor.fetchone()
    conn.close()
    return render_template('edit_company.html', company=company)


# DELETE - Remove a company
@app.route('/companies/delete/<int:id>')
def delete_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('companies'))


# -------------------- JOBS --------------------

# READ - List all jobs with company names
@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT jobs.*, companies.company_name
        FROM jobs
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    """)
    all_jobs = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=all_jobs)


# CREATE - Add a new job
@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        requirements = request.form['requirements']
        if requirements:
            req_list = [r.strip() for r in requirements.split(',')]
            requirements = json.dumps(req_list)
        else:
            requirements = None
        sql = """INSERT INTO jobs
                 (company_id, job_title, job_type, salary_min, salary_max,
                  job_url, date_posted, requirements)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form['salary_min'] or None,
            request.form['salary_max'] or None,
            request.form['job_url'],
            request.form['date_posted'] or None,
            requirements
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))
    cursor.execute("SELECT * FROM companies")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('add_job.html', companies=companies_list)


# UPDATE - Edit an existing job
@app.route('/jobs/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        requirements = request.form['requirements']
        if requirements:
            req_list = [r.strip() for r in requirements.split(',')]
            requirements = json.dumps(req_list)
        else:
            requirements = None
        sql = """UPDATE jobs SET
                 company_id=%s, job_title=%s, job_type=%s,
                 salary_min=%s, salary_max=%s, job_url=%s,
                 date_posted=%s, requirements=%s
                 WHERE job_id=%s"""
        values = (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form['salary_min'] or None,
            request.form['salary_max'] or None,
            request.form['job_url'],
            request.form['date_posted'] or None,
            requirements,
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (id,))
    job = cursor.fetchone()
    if job and job['requirements']:
        job['requirements'] = ', '.join(json.loads(job['requirements']))
    cursor.execute("SELECT * FROM companies")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('edit_job.html', job=job, companies=companies_list)


# DELETE - Remove a job
@app.route('/jobs/delete/<int:id>')
def delete_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('jobs'))


# -------------------- APPLICATIONS --------------------

# READ - List all applications with job titles and company names
@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        LEFT JOIN jobs ON applications.job_id = jobs.job_id
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    """)
    all_applications = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=all_applications)


# CREATE - Add a new application
@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """INSERT INTO applications
                 (job_id, application_date, status, resume_version,
                  cover_letter_sent, interview_data)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form['resume_version'],
            1 if request.form.get('cover_letter_sent') else 0,
            request.form['interview_data'] or None
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('applications'))
    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    """)
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template('add_application.html', jobs=jobs_list)


# UPDATE - Edit an existing application
@app.route('/applications/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """UPDATE applications SET
                 job_id=%s, application_date=%s, status=%s,
                 resume_version=%s, cover_letter_sent=%s, interview_data=%s
                 WHERE application_id=%s"""
        values = (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form['resume_version'],
            1 if request.form.get('cover_letter_sent') else 0,
            request.form['interview_data'] or None,
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('applications'))
    cursor.execute("SELECT * FROM applications WHERE application_id = %s", (id,))
    application = cursor.fetchone()
    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    """)
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template('edit_application.html',
                           application=application, jobs=jobs_list)


# DELETE - Remove an application
@app.route('/applications/delete/<int:id>')
def delete_application(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('applications'))


# -------------------- CONTACTS --------------------

# READ - List all contacts with company names
@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        LEFT JOIN companies ON contacts.company_id = companies.company_id
    """)
    all_contacts = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=all_contacts)


# CREATE - Add a new contact
@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """INSERT INTO contacts
                 (company_id, contact_name, title, email, phone,
                  linkedin_url, notes)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['company_id'],
            request.form['contact_name'],
            request.form['title'],
            request.form['email'],
            request.form['phone'],
            request.form['linkedin_url'],
            request.form['notes']
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('contacts'))
    cursor.execute("SELECT * FROM companies")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('add_contact.html', companies=companies_list)


# UPDATE - Edit an existing contact
@app.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """UPDATE contacts SET
                 company_id=%s, contact_name=%s, title=%s,
                 email=%s, phone=%s, linkedin_url=%s, notes=%s
                 WHERE contact_id=%s"""
        values = (
            request.form['company_id'],
            request.form['contact_name'],
            request.form['title'],
            request.form['email'],
            request.form['phone'],
            request.form['linkedin_url'],
            request.form['notes'],
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return redirect(url_for('contacts'))
    cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (id,))
    contact = cursor.fetchone()
    cursor.execute("SELECT * FROM companies")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('edit_contact.html', contact=contact,
                           companies=companies_list)


# DELETE - Remove a contact
@app.route('/contacts/delete/<int:id>')
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('contacts'))


# -------------------- JOB MATCH --------------------

@app.route('/job_match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ''
    if request.method == 'POST':
        user_skills = request.form['skills']
        skill_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT jobs.*, companies.company_name
            FROM jobs
            LEFT JOIN companies ON jobs.company_id = companies.company_id
            WHERE jobs.requirements IS NOT NULL
        """)
        all_jobs = cursor.fetchall()
        conn.close()

        for job in all_jobs:
            try:
                requirements = json.loads(job['requirements'])
            except (json.JSONDecodeError, TypeError):
                continue

            req_lower = [r.lower() for r in requirements]
            matched = [s for s in skill_list if s in req_lower]
            missing = [r for r in requirements if r.lower() not in skill_list]
            total = len(req_lower)

            if total > 0:
                percentage = round((len(matched) / total) * 100)
                results.append({
                    'job_title': job['job_title'],
                    'company_name': job['company_name'],
                    'percentage': percentage,
                    'matched_count': len(matched),
                    'total_count': total,
                    'matched_skills': matched,
                    'missing_skills': missing
                })

        results.sort(key=lambda x: x['percentage'], reverse=True)

    return render_template('job_match.html', results=results,
                           user_skills=user_skills)


# -------------------- RUN APP --------------------

if __name__ == '__main__':
    app.run(debug=True)
