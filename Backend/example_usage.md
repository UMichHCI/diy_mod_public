# Email-Based Feed Processing Usage

The `process_json_custom_feed.py` script now accepts email addresses instead of user IDs, making it much more user-friendly for research studies.

## Examples

### 1. Process without saving (testing)
```bash
python process_json_custom_feed.py my_feed.json
```

### 2. Process and save for a user
```bash
python process_json_custom_feed.py my_feed.json --user-email participant1@study.edu --save
```

### 3. Process with custom title
```bash
python process_json_custom_feed.py my_feed.json \
  --user-email researcher@university.edu \
  --title "Study Condition A" \
  --save
```

### 4. Create example template
```bash
python process_json_custom_feed.py --create-example
```

## How it works

1. **Email Resolution**: The script automatically resolves the email to a user_id using the server
2. **Auto-Create Users**: If the email doesn't exist, a new user account is created automatically
3. **Feed Storage**: Both original and filtered feeds are stored with the resolved user_id
4. **Web Interface**: Users can then log in with the same email to view their feeds

## For User Studies

This makes the workflow much simpler:

1. **Researcher**: Processes feeds using participant emails
   ```bash
   python process_json_custom_feed.py study_feed.json --user-email participant1@test.com --save
   ```

2. **Participant**: Logs into web interface using the same email
   - Goes to the web app
   - Enters `participant1@test.com`
   - Sees their comparison feeds automatically

## Requirements

- Backend server must be running (`python app.py`)
- Email must be valid format (contains @ and domain)
- Use `--save` flag to store in database