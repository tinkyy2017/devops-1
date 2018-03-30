# -*- coding:utf-8 -*-

import uuid

from django.db import models
from accounts.models import User
from django.contrib.auth.models import Permission


class IDC(models.Model):
    """add IDC table"""
    IDC_OPERATOR_CHOICES = (
        (1, '电信'),
        (2, '联通'),
        (3, '移动'),
        (4, '铁通'),
        (5, '其他'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=64, verbose_name='机房名')
    address = models.CharField(max_length=128, verbose_name='所在地址')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='联系电话')
    manage_user = models.ForeignKey(User, blank=True, null=True, verbose_name='管理人')
    network = models.CharField(max_length=32, blank=True, null=True, verbose_name='所在网段')
    operator = models.SmallIntegerField(choices=IDC_OPERATOR_CHOICES, default=1, verbose_name='运营商')
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='描述')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ('get_idc', ('查看机房')),
        #     ('add_idc', ('添加机房')),
        #     ('edit_idc', ('编辑机房')),
        #     ('del_idc', ('删除机房')),
        # )
        # default_permissions = ()

    def __str__(self):
        return self.name


class AssetGroup(models.Model):
    """add HostGroup table"""
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=32, unique=True, verbose_name='主机组')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='描述')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '资产组'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ('get_assetgroup', ('查看资产组')),
        #     ('add_assetgroup', ('添加资产组')),
        #     ('edit_assetgroup', ('编辑资产组')),
        #     ('del_assetgroup', ('删除资产组')),
        # )
        # default_permissions = ()

    def __str__(self):
        return self.name


class Asset(models.Model):
    """Add asset table"""
    ASSET_TYPE_CHOICES = (
        ('server', '服务器'),
        ('virtual machine', '虚拟机'),
        ('other', 'Other'),
    )
    ASSET_STATUS_CHOICES = (
        ('normal', '正常'),
        ('measure', '故障'),
        ('other', 'Other')
    )
    OS_TYPE_CHOICES = (
        ('centos', 'Centos'),
        ('macos', 'MacOs'),
        ('ubuntu', 'Ubuntu'),
        ('windows', 'Windows'),
        ('other', 'Other')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name='ID')
    asset_name = models.CharField(max_length=64, unique=True, verbose_name='资产名')
    manage_ipaddress = models.GenericIPAddressField(unique=True, verbose_name='管理IP')
    other_ipaddress = models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='其他IP')
    asset_type = models.CharField(max_length=32, choices=ASSET_TYPE_CHOICES, default='server', verbose_name='资产类型')
    macaddress = models.CharField(max_length=32, blank=True, null=True, verbose_name='MAC地址')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='厂商')
    port_num = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='端口个数')
    os_type = models.CharField(max_length=32, default='', choices=OS_TYPE_CHOICES, verbose_name='系统类型')
    os_version = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统版本')

    idc = models.ForeignKey(IDC, related_name='asset_idc', blank=True, null=True, verbose_name='所在机房')
    asset_group = models.ManyToManyField(AssetGroup, related_name='asset_group', verbose_name='资产组')
    manage_user = models.ForeignKey(User, related_name='asset_user', blank=True, null=True, verbose_name='管理人')

    # disk = models.OneToOneField('Disk', blank=True, null=True, verbose_name='磁盘信息')
    # memory = models.OneToOneField('Memory', blank=True, null=True, verbose_name='内存信息')
    # cpu = models.OneToOneField('Cpu', blank=True, null=True, verbose_name='Cpu信息')

    mem_total = models.IntegerField(blank=True, null=True, verbose_name='内存总数')
    mem_free = models.IntegerField(blank=True, null=True, verbose_name='内存空闲数')
    mem_buffers = models.IntegerField(blank=True, null=True, verbose_name='buffers内存数')
    mem_cached = models.IntegerField(blank=True, null=True, verbose_name='cached内存数')
    mem_available = models.IntegerField(blank=True, null=True, verbose_name='可用内存数')
    mem_used = models.IntegerField(blank=True, null=True, verbose_name='已使用内存数')
    swap_mem_total = models.IntegerField(blank=True, null=True, verbose_name='虚拟内存数')
    swap_mem_free = models.IntegerField(blank=True, null=True, verbose_name='虚拟内存空闲数')
    swap_mem_used = models.IntegerField(blank=True, null=True, verbose_name='已使用虚拟内存数')

    logical_num = models.IntegerField(blank=True, null=True, verbose_name='逻辑CPU个数')
    physical_num = models.IntegerField(blank=True, null=True, verbose_name='物理CPU个数')
    vendor = models.CharField(max_length=64, blank=True, null=True, verbose_name='CPU厂商')
    model_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='CPU型号')
    cpu_cores = models.IntegerField(blank=True, null=True, verbose_name='每个CPU核数')

    disk_size = models.IntegerField(default=0, blank=True, null=True, verbose_name='磁盘大小')
    disk_used = models.IntegerField(default=0, blank=True, null=True, verbose_name='已使用磁盘大小')
    disk_free = models.IntegerField(default=0, blank=True, null=True, verbose_name='空闲磁盘大小')

    status = models.CharField(max_length=32, choices=ASSET_STATUS_CHOICES, default='normal', verbose_name='状态')
    description = models.TextField(max_length=256, null=True, blank=True, verbose_name='描述')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ('get_asset', ('查看资产')),
        #     ('add_asset', ('添加资产')),
        #     ('edit_asset', ('编辑资产')),
        #     ('del_asset', ('删除资产')),
        # )
        # default_permissions = ()

    def __str__(self):
        return '{} sn:{}'.format(self.asset_name, self.sn)




