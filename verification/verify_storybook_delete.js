import { chromium } from 'playwright';
import { spawn } from 'child_process';
import waitOn from 'wait-on';

async function runVerification() {
  console.log('Starting verification...');

  const server = spawn('pnpm', ['--dir', 'ui-kit-react', 'preview', '--', '--port', '4173'], {
    stdio: 'inherit',
    shell: true
  });

  try {
    await waitOn({ resources: ['tcp:4173'], timeout: 10000 });
    console.log('Server ready at http://localhost:4173');

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.route('**/api/screenwriting/storybook', async route => {
      const json = {
        documents: [
          {
            id: 'doc1',
            name: 'Test Document To Delete',
            description: 'This document should be deleted',
            uploaded_at: new Date().toISOString(),
            tags: ['test'],
            chapters: []
          }
        ]
      };
      await route.fulfill({ json });
    });

    await page.route('**/api/screenwriting/storybook/delete', async route => {
       if (route.request().method() === 'POST') {
         const postData = JSON.parse(route.request().postData());
         if (postData.id === 'doc1') {
            await route.fulfill({ status: 200, json: { ok: true } });
            return;
         }
       }
       await route.fulfill({ status: 500 });
    });

    await page.goto('http://localhost:4173');
    await page.click('button.agent-launcher');

    // DEBUG: Snapshot after click
    await page.waitForTimeout(1000);
    console.log(await page.content());

    // Maybe the selector is different
    const select = page.locator('select');
    if (await select.count() > 0) {
        await select.first().selectOption({ label: 'Screenwriting' });
    } else {
        console.log('No select element found');
    }

    // Wait for Storybook tab or content
    await page.click('button:has-text("Storybook")');

    // Wait for document list
    await page.waitForSelector('h4:has-text("Test Document To Delete")');
    console.log('Document found');

    // 1. Verify Delete Button on Card
    const deleteBtn = page.locator('.document-card-actions button.delete');
    await deleteBtn.waitFor({ state: 'visible' });

    // Mock window.confirm
    page.on('dialog', dialog => dialog.accept());

    // Click delete
    await deleteBtn.click();
    console.log('Clicked delete');

    // Wait for empty state
    await page.route('**/api/screenwriting/storybook', async route => {
        await route.fulfill({ json: { documents: [] } });
    });

    await page.waitForSelector('p.empty-state', { timeout: 10000 });
    console.log('Empty state found - Delete successful');

    await browser.close();
    console.log('Verification Passed');
  } catch (err) {
    console.error('Verification Failed:', err);
    process.exit(1);
  } finally {
    server.kill();
  }
}

runVerification();
