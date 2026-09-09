# CIVL 2050 Fall 2026 build change log

This log records source changes that affect the syllabus, schedule, course map, or other student-facing build outputs. Generated files are not edited directly.

## 2026-08-28

### Akib Arafin and Jing Zhang office hours

- Akib Arafin: Monday 12:00--3:00 PM in JEC 5318.
- Jing Zhang: Thursday 12:00--3:00 PM in JEC 5308, unchanged from his previously proposed time.
- Removed the student-facing Webex-room links for Akib and Jing.

## 2026-08-26

### Late-submission table alignment

- Left-aligned the Late Submissions table with the surrounding policy text and other narrative tables.
- Moved Final Grade Rounding to begin on page 4.
- Integrated the laboratory pass requirement into the preceding laboratory overview paragraph.
- Started Homework Presentation on a fresh page and rebalanced the following page breaks to prevent dangling headings.

### Attendance and final class

- Attendance will be recorded in the Blackboard Attendance tool.
- Exam 1 and Exam 2 are exempt course-wide meetings. All other scheduled class meetings count unless Daniel later exempts a meeting.
- Removed the fixed attendance denominator and fixed per-absence deduction from student-facing policy language.
- Clarified Blackboard terminology: an individual student may be marked Excused; a course-wide meeting is Exempt.
- Blackboard Late status is set at 50\% attendance credit for the meeting.
- Reconciled the canonical schedule: Dec. 7 is course synthesis/problem-solving buffer; Dec. 10 is Class 28/final-exam review and the last scheduled CIVL 2050 meeting.

### Anu Aryal office hours

- Confirmed office: JEC 5304.
- Confirmed office hours: Tuesday 9:00 AM--12:00 PM.

### Syllabus - table layout system

- Source changed: `main.tex`, `sections/course_info.tex`, and `scripts/generate_tables.py`.
- Logic: all student-facing tables use the printable text width; narrative fields are ragged-right; short labels, counts, and percentages are centered; outer padding and vertical rules are omitted; flexible narrative columns absorb unused width.
- Spacing: increased global inter-column padding from 3.5 pt to 4 pt and rebalanced fixed columns to reduce awkward wrapping while using the full page.
- Letter-grade table: converted from a narrow fixed-width table to a full-width `tabularx` table.
- Laboratory table: changed from one compressed multi-line row per experiment to an experiment-first block with separate section rows and explicit Hour 1/Hour 2 windows.
- Release status: source updated; rebuild remains a draft pending calendar reconciliation and final TA office-hour assignments.

### Instructor office correction

- Permanent office: JEC 4030.
- Office hours: Wednesday 2:00--4:30 PM in JROWL 2C13.
- Removed the incorrect implication that JROWL 2C13 is Daniel's permanent office.
- TA availability is not treated as a finalized recurring office-hour assignment.

### Syllabus - section planning data

- Source changed: `CIVL2050_F26_syllabus_v0_3/sections/course_info.tex`
- Change: Removed the Section Planning Data table. Enrollment and capacity planning are administrative information and are not relevant to students.
- Resulting outputs: Live build `CIVL2050_F26_syllabus_v0_3/main.pdf`; staged export `Syllabus/Syllabus F26/CIVL2050_F26_syllabus_v2_DRAFT.pdf`.
- Verification: Rebuilt successfully; seven letter-size pages; source text confirms the planning table is absent; revised pages 1-2 visually checked with no clipping or overflow.
- Release status: Not published; student-visible status not confirmed.

### Office hours

- Confirmed in current source: Daniel Lander - JEC 4030, Wednesday 2:00-4:30 PM, with Webex link.
- Still unresolved in accessible source: Anu Aryal's office and office-hour time; Akib Arafin's office-hour time; Jing Zhang's office-hour time.
- No placeholder was replaced without confirmed details.
