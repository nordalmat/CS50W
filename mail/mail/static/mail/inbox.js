document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Compose Submit
  document.querySelector('#compose-form').addEventListener('submit', sent_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#item-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function open_email(id) {
  console.log(id)
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#item-view').style.display = 'block';

    document.querySelector('#item-view').innerHTML = `
      <ul class='list-group'>
        <li class='list-group-item border-0 mb-auto'><strong>From: </strong>${email.sender}</li>
        <li class='list-group-item border-0 mb-auto'><strong>To: </strong>${email.recipients}</li>
        <li class='list-group-item border-0 mb-auto'><strong>Subject: </strong>${email.subject}</li>
        <li class='list-group-item border-0 mb-auto'><strong>Timestamp: </strong>${email.timestamp}</li>
        <li class='list-group-item border-0 mb-auto'><hr></li>
        <li class='list-group-item border-0 mb-auto'>${email.body}</li>
      </ul>
    `
    // Change to read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    
    // Archive-Unarchive
    if (email.sender !== document.querySelector('#user').innerHTML) {
      const archive_element = document.createElement('button');
      archive_element.innerHTML = email.archived ? "Unarchive" : "Archive";
      archive_element.className = email.archived ? "btn btn-outline-primary mx-3 my-3" : "btn btn-primary mx-3 my-3";
      archive_element.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => { open_email(email.id)})
      })
      document.querySelector('#item-view').append(archive_element);
    }

    const reply_element = document.createElement('button');
    reply_element.innerHTML = 'Reply';
    reply_element.className = "btn btn-outline-primary mx-3 my-3"
    document.querySelector('#item-view').append(reply_element);
    reply_element.addEventListener('click', function() { 
      compose_email()
    
      // Pre-fill composition fields
      document.querySelector('#compose-recipients').value = email.sender;
      let subject = email.subject
      if (subject.split(' ')[0] !== 'Re:') {
        subject = `Re: ${email.subject}`
      } 
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n  ${email.body}\n\n`;
    });
  });
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#item-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Receive latest email list, show the mailbox entries
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    emails.forEach(item => {
      const element = document.createElement('div');
      element.className = "list-group-item my-3 flex-column align-items-start";
      element.innerHTML = `
        <div class="d-flex w-100 justify-content-between my-1 border border-dark rounded">
          <strong class="mb-1 my-1 mx-3">${item.sender}</strong>
          <p class="mb-1 my-auto mx-3">${item.subject}</p>
          <p class="mb-1 my-auto mx-3">${item.timestamp}</p>
        </div>
      `;
      // Manage read (unread) logic
      if (item.read === true) {
        element.className = 'read'
      } else {
        element.className = 'unread'
      }

      // Manage click
      element.addEventListener('click', function() {
        open_email(item.id)
      });
      document.querySelector('#emails-view').append(element);

    });

});

}

function sent_email(event) {
  event.preventDefault();
  // Receive form data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send POST request of new email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      load_mailbox('sent');
  });
  
}
