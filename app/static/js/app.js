/**
 * app.js – StudyTrack client-side JavaScript.
 * Handles sidebar toggle, edit modals, and auto-dismiss alerts.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ======== Sidebar Toggle (mobile) ========
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function (e) {
            if (window.innerWidth < 768 && sidebar.classList.contains('show')) {
                if (!sidebar.contains(e.target) && e.target !== sidebarToggle) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }

    // ======== Auto-dismiss alerts after 5 seconds ========
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ======== Edit Assignment Modal – Fetch data via API ========
    document.querySelectorAll('.edit-assignment-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var id = this.getAttribute('data-id');
            fetch('/api/assignment/' + id)
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.error) { alert('Assignment not found.'); return; }
                    document.getElementById('editTitle').value = data.title;
                    document.getElementById('editSubject').value = data.subject;
                    document.getElementById('editDescription').value = data.description || '';
                    document.getElementById('editDueDate').value = data.due_date;
                    document.getElementById('editPriority').value = data.priority;
                    document.getElementById('editStatus').value = data.status;
                    document.getElementById('editAssignmentForm').action = '/assignments/edit/' + id;
                })
                .catch(function (err) { console.error('Error fetching assignment:', err); });
        });
    });

    // ======== Edit Exam Modal – Fetch data via API ========
    document.querySelectorAll('.edit-exam-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var id = this.getAttribute('data-id');
            fetch('/api/exam/' + id)
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.error) { alert('Exam not found.'); return; }
                    document.getElementById('editExamTitle').value = data.title;
                    document.getElementById('editExamSubject').value = data.subject;
                    document.getElementById('editExamType').value = data.exam_type;
                    document.getElementById('editExamDate').value = data.exam_date;
                    document.getElementById('editExamTime').value = data.exam_time || '';
                    document.getElementById('editExamSyllabus').value = data.syllabus || '';
                    document.getElementById('editExamVenue').value = data.venue || '';
                    document.getElementById('editExamForm').action = '/exams/edit/' + id;
                })
                .catch(function (err) { console.error('Error fetching exam:', err); });
        });
    });

});
