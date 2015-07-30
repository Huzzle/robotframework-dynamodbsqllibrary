#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Amazon DynamoDB SQL Library - an Amazon DynamoDB testing library with SQL-like DSL.
#    Copyright (C) 2014 - 2015  Richard Huang <rickypc@users.noreply.github.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Amazon DynamoDB SQL Library - an Amazon DynamoDB testing library with SQL-like DSL.
"""

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.utils import ConnectionCache
from sys import path
path.append('src')
from DynamoDBSQLLibrary.keywords import SessionManager
import unittest


class SessionManagerTests(unittest.TestCase):
    """Session Manager keyword test class."""

    def setUp(self):
        """Instantiate the session manager class."""
        self.label = 'MY-LABEL'
        self.region = 'MY-REGION'
        self.session = SessionManager()

    def test_class_should_initiate(self):
        """Class init should instantiate required classes."""
        self.assertIsInstance(self.session._builtin, BuiltIn)
        self.assertIsInstance(self.session._cache, ConnectionCache)
        self.assertIsInstance(self.session._string, String)

    def test_create_should_register_new_session(self):
        """Create session should successfully register new session."""
        label = self.session.create_dynamodb_session(self.region, label=self.label)
        self.assertEqual(label, self.label)
        self.assertNotEqual(label, self.region)
        try:
            self.session._cache.switch(label)
        except RuntimeError:
            self.fail("Label '%s' should be exist." % label)
        self.session.delete_all_dynamodb_sessions()

    def test_create_should_register_with_region_as_label(self):
        """Create session should successfully register new session with region as default label."""
        label = self.session.create_dynamodb_session(self.region)
        self.assertNotEqual(label, self.label)
        self.assertEqual(label, self.region)
        try:
            self.session._cache.switch(label)
        except RuntimeError:
            self.fail("Label '%s' should be exist." % label)
        self.session.delete_all_dynamodb_sessions()

    def test_delete_should_remove_all_sessions(self):
        """Delete session should successfully remove all existing sessions."""
        self.session.create_dynamodb_session(self.region, label=self.label)
        self.session.delete_all_dynamodb_sessions()
        with self.assertRaises(RuntimeError) as context:
            self.session._cache.switch(self.label)
        self.assertTrue("Non-existing index or alias '%s'." % self.label in context.exception)
