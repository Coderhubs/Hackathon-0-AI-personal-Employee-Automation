#!/usr/bin/env node

/**
 * Email MCP Server for AI Personal Employee
 * Provides email sending capabilities via Gmail
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import nodemailer from 'nodemailer';

// Email configuration from environment
const GMAIL_EMAIL = process.env.GMAIL_EMAIL;
const GMAIL_PASSWORD = process.env.GMAIL_PASSWORD;

// Create nodemailer transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: GMAIL_EMAIL,
    pass: GMAIL_PASSWORD,
  },
});

// Create MCP server
const server = new Server(
  {
    name: 'email-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'send_email',
        description: 'Send an email via Gmail',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject',
            },
            body: {
              type: 'string',
              description: 'Email body (plain text or HTML)',
            },
            html: {
              type: 'boolean',
              description: 'Whether body is HTML (default: false)',
              default: false,
            },
          },
          required: ['to', 'subject', 'body'],
        },
      },
      {
        name: 'draft_email',
        description: 'Create a draft email (does not send)',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject',
            },
            body: {
              type: 'string',
              description: 'Email body',
            },
          },
          required: ['to', 'subject', 'body'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'send_email') {
      const { to, subject, body, html = false } = args;

      // Validate inputs
      if (!to || !subject || !body) {
        throw new Error('Missing required fields: to, subject, body');
      }

      // Send email
      const mailOptions = {
        from: GMAIL_EMAIL,
        to,
        subject,
        [html ? 'html' : 'text']: body,
      };

      const info = await transporter.sendMail(mailOptions);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              messageId: info.messageId,
              to,
              subject,
              timestamp: new Date().toISOString(),
            }, null, 2),
          },
        ],
      };
    }

    if (name === 'draft_email') {
      const { to, subject, body } = args;

      // Validate inputs
      if (!to || !subject || !body) {
        throw new Error('Missing required fields: to, subject, body');
      }

      // Create draft (just return the draft, don't send)
      const draft = {
        to,
        subject,
        body,
        created: new Date().toISOString(),
        status: 'draft',
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              draft,
              message: 'Draft created. Use send_email to send after approval.',
            }, null, 2),
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: false,
            error: error.message,
          }, null, 2),
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Email MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
