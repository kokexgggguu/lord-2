# Discord Server Manager Bot

## Overview

A comprehensive Discord server management platform consisting of a Flask web dashboard and a Discord bot with advanced features. The bot provides match scheduling capabilities, multi-language support, server administration tools, and comprehensive logging. The application includes a web-based control panel for monitoring bot activities, viewing statistics, and managing server configurations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Dual-Application Architecture
- **Flask Web Application**: Provides web dashboard and REST API endpoints for bot monitoring and management
- **Discord Bot**: Handles all Discord interactions using discord.py with slash command support
- **Threading Model**: Bot and web server run concurrently in separate threads for optimal performance
- **Keep-Alive System**: Dedicated web server endpoint for uptime monitoring

### Backend Architecture
- **SQLAlchemy ORM**: Database abstraction with declarative models for data persistence
- **Database Models**: Server, Match, MatchReminder, BotLog with proper relationships and foreign keys
- **Scheduler Integration**: APScheduler for automated match reminders and periodic tasks
- **Multi-language Translation System**: Built-in support for English, Portuguese, and Spanish

### Discord Bot Features
- **Slash Commands**: Modern Discord interaction system with comprehensive command structure
- **Match Management**: Complete match lifecycle with creation, listing, and termination capabilities
- **Automated Reminders**: 10-minute and 3-minute alerts before matches with timezone conversion
- **Translation Interface**: Interactive buttons for real-time message translation
- **Channel Restrictions**: Admin-configurable channel permissions for bot usage
- **Activity Logging**: Comprehensive logging of all bot interactions and commands

### Web Dashboard Components
- **Real-time Statistics**: Server count, active matches, command usage metrics
- **Match Management**: View all matches with pagination, filtering, and status tracking
- **Log Viewer**: Filterable activity logs with server-specific views
- **Server Configuration**: Management interface for Discord server settings
- **Interactive Charts**: Data visualization for bot usage patterns and activity trends

### Data Storage Architecture
- **SQLite/PostgreSQL**: Configurable database backend with connection pooling
- **Relationship Management**: Cascading deletes and proper foreign key constraints
- **Migration Support**: Database schema evolution with SQLAlchemy migrations
- **Backup Strategy**: Automated data persistence with transaction management

### Security and Authorization
- **Environment Variables**: Secure configuration management for sensitive data
- **Guild-based Permissions**: Server-specific command restrictions and channel controls
- **Admin-only Commands**: Protected administrative functions with permission checking
- **Rate Limiting**: Built-in protection against command spam and abuse

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework for dashboard and API endpoints
- **discord.py**: Discord API wrapper for bot functionality
- **SQLAlchemy**: ORM for database operations and model management
- **APScheduler**: Task scheduling for automated reminders and periodic jobs

### Database and Storage
- **SQLite**: Default database for development and small deployments
- **PostgreSQL**: Production database option with advanced features
- **Werkzeug**: WSGI utilities and development server

### Timezone and Localization
- **pytz**: Timezone conversion and handling for global match scheduling
- **Custom Translation System**: Multi-language support with dynamic message translation

### Development and Deployment
- **python-dotenv**: Environment variable management
- **Gunicorn**: Production WSGI server for web application deployment
- **psutil**: System monitoring and performance metrics

### Frontend Technologies
- **Bootstrap**: Responsive UI framework with dark theme support
- **Chart.js**: Interactive data visualization for dashboard statistics
- **Font Awesome**: Icon library for enhanced user interface
- **JavaScript**: Client-side functionality for dynamic dashboard features

## Recent Changes
- ✅ استخراج جميع الملفات من مجلد DiscordBotMaker وإعادة تنظيمها
- ✅ إصلاح جميع مشاكل البنية والاستيراد في المشروع  
- ✅ إضافة DISCORD_TOKEN في Replit Secrets بشكل آمن
- ✅ إنشاء بوت ديسكورد شامل وفعال (discord_bot_working.py)
- ✅ تشغيل البوت بنجاح مع 9 slash commands متزامنة
- ✅ تطبيق Flask يعمل على المنفذ 5000 مع واجهة إدارة كاملة
- ✅ نظام قاعدة بيانات SQLite يعمل مع API endpoints
- ✅ البوت متصل بـ 2 خوادم ديسكورد ويعمل بشكل مثالي
- ✅ إضافة جميع الأوامر الأساسية: ping, help, serverinfo, userinfo, avatar, 8ball
- ✅ إضافة جميع أوامر الإدارة: kick, ban, unban, timeout, untimeout, warn, clear
- ✅ إضافة أوامر المساعدة: say, embed, roleinfo, channelinfo  
- ✅ إضافة أوامر المباريات: create_match, list_matches, end_match
- ✅ تطبيق نظام سجلات شامل لجميع الأوامر المستخدمة
- ✅ إضافة جميع الـ 16 أمر المطلوبة مع معالجة شاملة للأخطاء

## Bot Features Available

### Complete Command List (16 Total Commands):

**🔧 Basic Commands:**
- `/ping` - Check bot latency and status
- `/help` - Show all available commands
- `/serverinfo` - Display server information
- `/userinfo` - Show user information
- `/avatar` - Display user's avatar
- `/8ball` - Ask the magic 8-ball

**🛡️ Moderation Commands:**
- `/kick` - Kick a member from server
- `/ban` - Ban a member from server  
- `/unban` - Unban a user by ID
- `/timeout` - Timeout a member
- `/untimeout` - Remove timeout from member
- `/warn` - Warn a member (with DM)
- `/clear` - Clear messages from channel

**🔧 Utility Commands:**
- `/say` - Make the bot say something
- `/embed` - Create custom embed messages
- `/roleinfo` - Show detailed role information
- `/channelinfo` - Show channel information

**⚽ Match Management:**
- `/create_match` - Create scheduled matches
- `/list_matches` - List active matches
- `/end_match` - End a match by ID

### Additional Features:
- Web dashboard with real-time statistics
- Multi-server support with individual guild management
- Comprehensive activity logging system
- Real-time bot status monitoring
- Match reminder system with automated DMs
- Multi-language translation support
- Channel permission restrictions
- Database integration with SQLite