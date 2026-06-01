import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set page configuration for a premium layout
st.set_page_config(page_title="Smart Campus Dashboard", layout="wide")

# Helper function to dynamically evaluate Grade and Remark based on Score
def get_grade_and_remark(score):
    if score >= 90:
        return "A", "Outstanding Performance"
    elif score >= 75:
        return "B", "Good Progress"
    elif score >= 60:
        return "C", "Satisfactory Summary"
    else:
        return "D", "Needs Academic Focus"

# -------------------------------------------------------------------
# ASSIGNMENT Q7: USER-DEFINED EXCEPTION CLASS
# -------------------------------------------------------------------
class MissingFileOrFolderError(Exception):
    """Raised when a required file or folder is missing in the directory."""
    pass

# -------------------------------------------------------------------
# STATE MANAGEMENT (Simulating a database)
# -------------------------------------------------------------------
if "students" not in st.session_state:
    st.session_state.students = [
        {"ID": "101", "Name": "Shantha", "Subject": "Python Programming", "Score": 95, "Event_A": True, "Event_B": False},
        {"ID": "102", "Name": "Samriddhi", "Subject": "Introduction to AI", "Score": 98, "Event_A": True, "Event_B": True},
        {"ID": "103", "Name": "Devansh", "Subject": "Mathematics", "Score": 92, "Event_A": False, "Event_B": True},
        {"ID": "104", "Name": "Siddhi", "Subject": "English", "Score": 88, "Event_A": False, "Event_B": False},
        {"ID": "105", "Name": "Rahul", "Subject": "Physics", "Score": 76, "Event_A": True, "Event_B": True},
        {"ID": "106", "Name": "Priya", "Subject": "Mathematics", "Score": 84, "Event_A": False, "Event_B": False},
    ]

if "courses" not in st.session_state:
    st.session_state.courses = []

if "guests" not in st.session_state:
    st.session_state.guests = []

# -------------------------------------------------------------------
# HEADER & STYLING
# -------------------------------------------------------------------
st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center;">
        <h1 style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif;">🏫 Smart Campus Information & Analytics System</h1>
        <p style="color: #e0e0e0; margin: 5px 0 0 0;">Premium Student Management, Registration, Ledger & Annual Insights</p>
    </div>
""", unsafe_allow_html=True)

# Tabs menu matching your app structure
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Student Dashboard", 
    "📚 Course Registration", 
    "📁 Directory Scanner",
    "🔍 Search Student ID", 
    "🎉 Campus Events Manager", 
    "💳 Fees Ledger",
    "📊 Final Annual Report"
])

# -------------------------------------------------------------------
# SECTION 1: STUDENT DASHBOARD
# -------------------------------------------------------------------
with tab1:
    st.header("🎓 Student Dashboard")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Student")
        with st.form("student_form", clear_on_submit=True):
            reg_num = st.text_input("Registration Number")
            st_name = st.text_input("Student Name")
            subject = st.selectbox("Select Subject", ["Introduction to AI", "Python Programming", "Mathematics", "English", "Physics"])
            score = st.number_input("Subject Score", min_value=0, max_value=100, step=1)
            
            submit_btn = st.form_submit_button("Register Student")
            if submit_btn:
                if reg_num.strip() == "" or st_name.strip() == "":
                    st.error("Registration number and Name cannot be blank.")
                else:
                    if any(s["ID"] == reg_num for s in st.session_state.students):
                        st.error(f"Student with ID {reg_num} already exists.")
                    else:
                        new_student = {
                            "ID": reg_num,
                            "Name": st_name,
                            "Subject": subject,
                            "Score": score,
                            "Event_A": False,
                            "Event_B": False
                        }
                        st.session_state.students.append(new_student)
                        st.success(f"Registered {st_name} successfully!")
                        st.rerun()

    with col2:
        st.subheader("Student Database Matrix")
        if not st.session_state.students:
            st.info("No records present inside active database.")
        else:
            sort_opt = st.toggle("Sort Database Matrix by Student ID")
            display_list = list(st.session_state.students)
            if sort_opt:
                display_list = sorted(display_list, key=lambda x: x["ID"])
                
            h_id, h_name, h_sub, h_score, h_grade, h_rem, h_act = st.columns([1, 1.5, 2, 1, 1, 2.5, 1.2])
            h_id.markdown("**ID**")
            h_name.markdown("**Name**")
            h_sub.markdown("**Subject**")
            h_score.markdown("**Marks**")
            h_grade.markdown("**Grade**")
            h_rem.markdown("**Remark**")
            h_act.markdown("**Action**")
            st.markdown("<hr style='margin:4px 0 12px 0; border-top: 2px solid #cbd5e1;' />", unsafe_allow_html=True)
            
            for s in display_list:
                c_id, c_name, c_sub, c_score, c_grade, c_rem, c_act = st.columns([1, 1.5, 2, 1, 1, 2.5, 1.2])
                c_id.text(s["ID"])
                c_name.text(s["Name"])
                c_sub.text(s["Subject"])
                c_score.text(f"{s['Score']}/100")
                
                grade, remark = get_grade_and_remark(s["Score"])
                c_grade.text(grade)
                c_rem.caption(remark)
                
                if c_act.button("🗑️ Delete", key=f"del_{s['ID']}", type="secondary", use_container_width=True):
                    st.session_state.students = [item for item in st.session_state.students if item["ID"] != s["ID"]]
                    st.success(f"Removed ID: {s['ID']}")
                    st.rerun()
                st.markdown("<hr style='margin:4px 0;' />", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SECTION 2: COURSE REGISTRATION
# -------------------------------------------------------------------
with tab2:
    st.header("📚 Register New Course")
    cc1, cc2 = st.columns([1, 1])
    
    with cc1:
        st.subheader("Configure Course Parameters")
        with st.form("course_form", clear_on_submit=True):
            c_name = st.text_input("Course Name")
            c_credits = st.number_input("Course Credits", min_value=1, step=1)
            
            course_submit = st.form_submit_button("Register a new course")
            if course_submit:
                if c_name.strip() == "":
                    st.error("Course name is required")
                else:
                    st.session_state.courses.append({"Course Name": c_name, "Credits": c_credits})
                    st.success(f"Course '{c_name}' registered successfully.")
                    st.rerun()
                    
    with cc2:
        st.subheader("Registered Courses")
        if not st.session_state.courses:
            st.info("No active course modules enrolled.")
        else:
            st.table(pd.DataFrame(st.session_state.courses))
            total_credits = sum(item["Credits"] for item in st.session_state.courses)
            st.markdown(f"""
                <div style="background-color:#1e293b; padding:15px; border-radius:8px; border-left: 5px solid #3b82f6;">
                    <span style="color:#94a3b8; font-size:14px; display:block;">CUMULATIVE PROGRAM CREDITS</span>
                    <span style="color:#f8fafc; font-size:24px; font-weight:bold;">{total_credits} Credits Total</span>
                </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# SECTION 3: DIRECTORY SCANNER (MATCHING YOUR DESIGN INTERFACE)
# -------------------------------------------------------------------
with tab3:
    # Outer Premium Styled Card container to match your exact Canva blueprint UI layout
    st.markdown("""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 35px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 25px;">
            <span style="font-size: 45px;">📁</span>
            <h2 style="color: #1e3c72; margin: 10px 0 5px 0; font-family: sans-serif;">Directory Scanner</h2>
            <p style="color: #64748b; font-size: 14px; margin: 0 0 20px 0;">Enter a folder path to view all files inside it</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Positioned input layout
    directory_path = st.text_input("Project Folder Path Location:", value="./", help="Type a system path or leave as './' to scan current folder")
    
    # Styled activation engine button
    if st.button("Scan Directory", type="primary", use_container_width=True):
        scan_output = []
        
        try:
            # 1. Check if the path exists (Exception Requirement)
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Invalid directory path: {directory_path}")
            
            scan_output.append(f"Scanning directory: {directory_path}\n")
            
            # 2. Walk through the directory structure using your exact assignment parameters
            for root, dirs, files in os.walk(directory_path):
                level = root.replace(directory_path, "").count(os.sep)
                indent = " " * 4 * level
                scan_output.append(f"{indent}{os.path.basename(root)}/")
                
                sub_indent = " " * 4 * (level + 1)
                for f in files:
                    scan_output.append(f"{sub_indent}{f}")
                
                # 3. Custom User-Defined Exception Check
                if not files and not dirs:
                    raise MissingFileOrFolderError(f"Empty folder detected: {root}")
            
            # Success display
            st.success("📊 Architecture compilation successful!")
            st.code("\n".join(scan_output), language="text")
            
        # Complete Exception Handling Blocks matching your assignment rules exactly
        except FileNotFoundError as e:
            st.error(f"Error: {e}")
        except MissingFileOrFolderError as e:
            st.error(f"Custom Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

# -------------------------------------------------------------------
# SECTION 4: SEARCH STUDENT ID
# -------------------------------------------------------------------
with tab4:
    st.header("🔍 Search Student ID")
    search_query = st.text_input("Enter student registration id")
    if search_query:
        match = next((s for s in st.session_state.students if s["ID"].strip() == search_query.strip()), None)
        if match:
            st.success("Student registration id found")
            grade, remark = get_grade_and_remark(match["Score"])
            
            sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
            sc1.metric("Student ID", match["ID"])
            sc2.metric("Student Name", match["Name"])
            sc3.metric("Course Focus", match["Subject"])
            sc4.metric("Scores Evaluated", f"{match['Score']}/100")
            sc5.metric("Grade Earned", grade)
            sc6.metric("Performance Remark", remark)
        else:
            st.error("❌ The requested Student ID is not present in our records.")

# -------------------------------------------------------------------
# SECTION 5: CAMPUS EVENTS MANAGER
# -------------------------------------------------------------------
with tab5:
    st.header("🎉 Campus Events Manager")
    ec1, ec2 = st.columns([3, 2])
    
    with ec1:
        st.subheader("📋 Student participation in events")
        limit = min(6, len(st.session_state.students))
        for idx in range(limit):
            st_obj = st.session_state.students[idx]
            r_col1, r_col2, r_col3 = st.columns([2, 1, 1])
            r_col1.markdown(f"**{st_obj['Name']}** `(ID: {st_obj['ID']})`")
            st_obj["Event_A"] = r_col2.checkbox("Cultural Event", value=st_obj["Event_A"], key=f"evA_{st_obj['ID']}")
            st_obj["Event_B"] = r_col3.checkbox("Technical Event", value=st_obj["Event_B"], key=f"evB_{st_obj['ID']}")
            st.markdown("<hr style='margin:4px 0;' />", unsafe_allow_html=True)

    with ec2:
        st.subheader("👤 Outside Guest Sign-up")
        guest_name = st.text_input("Manually enter Outside Guest Name:", key="guest_input")
        g_btn1, g_btn2 = st.columns(2)
        if g_btn1.button("➕ Add to Cultural Event", use_container_width=True):
            if guest_name.strip():
                st.session_state.guests.append({"Name": guest_name, "Event_A": True, "Event_B": False})
                st.success(f"Added guest {guest_name} to Cultural Event")
                st.rerun()
        if g_btn2.button("➕ Add to Technical Event", use_container_width=True):
            if guest_name.strip():
                st.session_state.guests.append({"Name": guest_name, "Event_A": False, "Event_B": True})
                st.success(f"Added guest {guest_name} to Technical Event")
                st.rerun()

    list_a = [s["Name"] for s in st.session_state.students[:6] if s["Event_A"]] + [g["Name"] for g in st.session_state.guests if g["Event_A"]]
    list_b = [s["Name"] for s in st.session_state.students[:6] if s["Event_B"]] + [g["Name"] for g in st.session_state.guests if g["Event_B"]]
    overlap = list(set(list_a).intersection(set(list_b)))
    all_unique = list(set(list_a + list_b))

    box_col1, box_col2, box_col3, box_col4 = st.columns(4)
    
    with box_col1:
        items = "".join([f"<li>{name}</li>" for name in list_a]) if list_a else "<li>No registrations</li>"
        st.markdown(f'<div style="background-color: #e0f2fe; padding: 20px; border-radius: 10px; border-left: 6px solid #0284c7; min-height: 220px; color:#0369a1;"><h4>🔷 Cultural Event Attendees</h4><ul style="padding-left: 20px; margin:0;">{items}</ul></div>', unsafe_allow_html=True)

    with box_col2:
        items = "".join([f"<li>{name}</li>" for name in list_b]) if list_b else "<li>No registrations</li>"
        st.markdown(f'<div style="background-color: #f3e8ff; padding: 20px; border-radius: 10px; border-left: 6px solid #7e22ce; min-height: 220px; color:#6b21a8;"><h4>🔮 Technical Event Attendees</h4><ul style="padding-left: 20px; margin:0;">{items}</ul></div>', unsafe_allow_html=True)

    with box_col3:
        items = "".join([f"<li>{name}</li>" for name in overlap]) if overlap else "<p style='font-style: italic; margin:0;'>No overlaps found.</p>"
        st.markdown(f'<div style="background-color: #dcfce7; padding: 20px; border-radius: 10px; border-left: 6px solid #15803d; min-height: 220px; color:#166534;"><h4>📍 Common Students</h4><ul style="padding-left: 20px; margin:0;">{items}</ul></div>', unsafe_allow_html=True)

    with box_col4:
        items = "".join([f"<li>{name}</li>" for name in all_unique]) if all_unique else "<li>No participants tracking</li>"
        st.markdown(f'<div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 6px solid #f1f5f9; min-height: 220px; color:#f8fafc;"><h4>📋 All Unique Records</h4><p style="margin:0 0 10px 0; color:#94a3b8; font-size:20px;">Total: <b>{len(all_unique)}</b></p><ul style="padding-left: 20px; margin:0; font-size:13px; color:#cbd5e1;">{items}</ul></div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# SECTION 6: FEES LEDGER
# -------------------------------------------------------------------
with tab6:
    st.header("💳 Fees Ledger")
    lc1, lc2 = st.columns([1, 1])
    with lc1:
        t_fee = st.number_input("Tuition Base Fee", min_value=0.0, value=75000.0, step=500.0)
        h_fee = st.number_input("Hostel & Accommodation Fee", min_value=0.0, value=45000.0, step=500.0)
        p_fee = st.number_input("Transportation Route Fee", min_value=0.0, value=12000.0, step=500.0)
        compile_invoice = st.button("Calculate Total Fee", type="primary", use_container_width=True)
        
    with lc2:
        if compile_invoice:
            grand_total = t_fee + h_fee + p_fee
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); color: #f8fafc; border: 1px solid #334155;">
                    <p style="color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; margin: 0 0 15px 0;">Premium Balanced Invoice Statement</p>
                    <p style="margin: 5px 0; font-size:14px; color:#94a3b8;"><b>Tuition Base Fee:</b> ₹ {t_fee:,.2f}</p>
                    <p style="margin: 5px 0; font-size:14px; color:#94a3b8;"><b>Hostel Fee:</b> ₹ {h_fee:,.2f}</p>
                    <p style="margin: 5px 0; font-size:14px; color:#94a3b8;"><b>Transportation Fee:</b> ₹ {p_fee:,.2f}</p>
                    <hr style="border-top:1px solid #334155; margin:12px 0;"/>
                    <span style="font-size:12px; color:#cbd5e1; display:block;">GRAND COMPILATION BALANCE</span>
                    <h2 style="color: #f8fafc; font-size: 38px; margin: 0; font-family: monospace;">₹ {grand_total:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# SECTION 7: THE FINAL ANNUAL REPORT (Graphs & Aggregates)
# -------------------------------------------------------------------
with tab7:
    st.header("📊 Final Annual Report Dashboard")
    
    if not st.session_state.students:
        st.warning("Add records inside the dashboard tab to view aggregate data analysis maps.")
    else:
        raw_data = st.session_state.students
        total_eval_count = len(raw_data)
        global_scores = [s["Score"] for s in raw_data]
        global_avg = np.mean(global_scores)
        
        m_col1, m_col2 = st.columns(2)
        m_col1.metric("Total Students Evaluated", f"{total_eval_count} Profiles Tracking")
        m_col2.metric("Global Class Performance Mean Average", f"{global_avg:.2f}%")
        
        registered_dropdown_subjects = ["Introduction to AI", "Python Programming", "Mathematics", "English", "Physics"]
        subjects_mapped = {sub: [] for sub in registered_dropdown_subjects}
        
        for s in raw_data:
            sb = s["Subject"]
            if sb in subjects_mapped:
                subjects_mapped[sb].append({"Name": s["Name"], "Score": s["Score"]})
                
        stats_summary, toppers = {}, {}
        for sub in registered_dropdown_subjects:
            items = subjects_mapped[sub]
            if items:
                scores_list = [i["Score"] for i in items]
                stats_summary[sub] = {"Mean": np.mean(scores_list), "Median": np.median(scores_list), "Std": np.std(scores_list)}
                toppers[sub] = max(items, key=lambda x: x["Score"])
            else:
                stats_summary[sub] = {"Mean": 0.0, "Median": 0.0, "Std": 0.0}
                toppers[sub] = {"Name": "None Enrolled", "Score": 0}

        st.markdown("### 📈 Statistical Spread Summaries (Active System Focuses)")
        stat_cols = st.columns(5)
        for idx, sub in enumerate(registered_dropdown_subjects):
            values = stats_summary[sub]
            with stat_cols[idx]:
                st.markdown(f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); color:#1e293b; min-height: 160px;">
                        <h5 style="margin:0 0 8px 0; color:#1e3c72; border-bottom: 2px solid #f1f5f9; font-size:14px;">{sub}</h5>
                        <p style="margin:3px 0; font-size:12px;"><b>Mean:</b> {values["Mean"]:.1f}</p>
                        <p style="margin:3px 0; font-size:12px;"><b>Median:</b> {values["Median"]:.1f}</p>
                        <p style="margin:3px 0; font-size:12px;"><b>Std Dev:</b> {values["Std"]:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>### 🏆 Class Subject Toppers Podium", unsafe_allow_html=True)
        top_cols = st.columns(5)
        for idx, sub in enumerate(registered_dropdown_subjects):
            top_info = toppers[sub]
            with top_cols[idx]:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 12px; border-radius: 8px; text-align: center; min-height: 110px;">
                        <span style="font-size: 9px; font-weight: bold; text-transform: uppercase;">{sub}</span>
                        <h4 style="margin: 4px 0 0 0; color:white; font-size:14px;">🌟 {top_info["Name"]}</h4>
                        <p style="margin:0; font-size: 18px; font-weight: bold;">{top_info["Score"]}/100</p>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>### 📊 Visual Performance Metrics Graph", unsafe_allow_html=True)
        
        categories = list(stats_summary.keys())
        averages_to_plot = [v["Mean"] for v in stats_summary.values()]
        
        fig, ax = plt.subplots(figsize=(7, 3.5))
        colors = ["#3b82f6", "#10b981", "#8b5cf6", "#ec4899", "#f59e0b"]
        
        bars = ax.bar(categories, averages_to_plot, color=colors, width=0.45)
        
        ax.set_ylim(0, 105)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#94a3b8')
        ax.spines['bottom'].set_color('#94a3b8')
        ax.tick_params(colors='#475569', labelsize=8)
        plt.xticks(rotation=15, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 2, f'{height:.1f}%', 
                    va='bottom', ha='center', fontsize=8, fontweight='bold', color='#1e293b')
            
        st.pyplot(fig)
