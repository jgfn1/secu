.data
	_shellcmd: .string "/bin/bash"
	arg0: .string "bin/bash" 	@ args for shell command
	arg1: .string "-c"
	arg2: .string "echo $(date +%s) > access_time.txt"
	arg3: .zero 4
	all_args:
		.word arg0
		.word arg1
		.word arg2
		.word arg3

	msg: .zero 4

.text
	.global _start

_start:
	 bl _syscall
	 bl exit

_syscall:
	push {lr}
	mov r7, #11	@ execv syscall; exec shell command referenced by shellcmd
	ldr r0, =_shellcmd
	ldr r1, =all_args
	mov r2, #0
	svc #0
	pop {pc}

exit:
	mov r7, #1 			/*exit code*/
	mov r0, #0			/*returns 0 to the OS*/
	svc #0
