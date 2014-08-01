# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PromoterScore'
        db.create_table(u'promoterscore_promoterscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pypantry.Customer'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'promoterscore', ['PromoterScore'])


    def backwards(self, orm):
        # Deleting model 'PromoterScore'
        db.delete_table(u'promoterscore_promoterscore')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'marketing.offer': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Offer'},
            'apply_product_limit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_vip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_shipment_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['marketing.PriceList']", 'null': 'True', 'blank': 'True'}),
            'product_discount': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '4', 'decimal_places': '2'}),
            'shipping_offer': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('ckeditor.fields.RichTextField', [], {})
        },
        u'marketing.pricelist': {
            'Meta': {'object_name': 'PriceList'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price_list': ('marketing.models.ProductPriceField', [], {})
        },
        u'product.brand': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Brand'},
            'canonical_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.TextField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'product.category': {
            'Meta': {'ordering': "('status', 'order')", 'object_name': 'Category'},
            'brands': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['product.Brand']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'product.fixedschedule': {
            'Meta': {'ordering': "('quantity', 'send_every_months')", 'unique_together': "(('quantity', 'send_every_months'),)", 'object_name': 'FixedSchedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'send_every_months': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'product.preference': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('key', 'brand'),)", 'object_name': 'Preference'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'preferences'", 'to': u"orm['product.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'max_choices': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'min_choices': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'product.preferencevalue': {
            'Meta': {'ordering': "('preference__brand__name', 'preference__name', 'label')", 'object_name': 'PreferenceValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'preference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['product.Preference']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'product.product': {
            'Meta': {'ordering': "('brand__name', 'name')", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Brand']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Category']", 'through': u"orm['product.ProductCategory']", 'symmetrical': 'False'}),
            'cogs': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '12', 'decimal_places': '2'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.FixedSchedule']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '12', 'decimal_places': '2'}),
            'max_in_first_shipment': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            'max_offer_qty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '4'}),
            'max_per_shipment': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_product': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'refill_product'", 'null': 'True', 'blank': 'True', 'to': u"orm['product.Product']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '12', 'decimal_places': '2'}),
            'qty_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'secondary_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'product.productcategory': {
            'Meta': {'unique_together': "(('category', 'position'), ('product', 'category'))", 'object_name': 'ProductCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Product']"})
        },
        u'promoterscore.promoterscore': {
            'Meta': {'object_name': 'PromoterScore'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pypantry.Customer']"})
        },
        u'pypantry.address': {
            'Meta': {'object_name': 'Address'},
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'addr2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'tg_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        },
        u'pypantry.customer': {
            'Meta': {'object_name': 'Customer'},
            'account_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'checked_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'churn_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'do_not_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'member_since': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['marketing.Offer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'pantry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'customer_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['pypantry.Pantry']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'ship_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ship_customer_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['pypantry.Address']"}),
            'shipping_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'stripe_token': ('utils.fields.CharNullField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'tg_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tracking_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'pypantry.pantry': {
            'Meta': {'object_name': 'Pantry'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['questions.Answer']", 'symmetrical': 'False'}),
            'brands': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Brand']", 'symmetrical': 'False'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'primary_pantry'", 'unique': 'True', 'null': 'True', 'to': u"orm['pypantry.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper_brand': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paper_pantry_set'", 'null': 'True', 'to': u"orm['product.Brand']"}),
            'preferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.PreferenceValue']", 'symmetrical': 'False'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Product']", 'symmetrical': 'False'}),
            'soap_brand': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'soap_pantry_set'", 'null': 'True', 'to': u"orm['product.Brand']"})
        },
        u'questions.answer': {
            'Meta': {'object_name': 'Answer'},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questions.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'blank': 'True'})
        },
        u'questions.question': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['promoterscore']